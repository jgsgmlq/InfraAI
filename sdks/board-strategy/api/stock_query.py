"""
AKShare 行情查询封装

提供股票量价数据查询功能，支持单只和批量查询。
"""

import sys
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time


class StockQueryError(Exception):
    """股票查询异常"""
    pass


class StockDataQuery:
    """股票数据查询类"""

    def __init__(self, cache_enabled: bool = True, cache_ttl: int = 3600):
        """
        初始化查询器

        Args:
            cache_enabled: 是否启用缓存
            cache_ttl: 缓存过期时间（秒）
        """
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple] = {}  # key -> (data, timestamp)

        # 延迟导入 akshare，避免在测试时必须安装
        try:
            import akshare as ak
            self.ak = ak
        except ImportError:
            print("警告: akshare 未安装，请运行: pip install akshare", file=sys.stderr)
            self.ak = None

    def _get_cache_key(self, code: str, date: str) -> str:
        """生成缓存键"""
        return f"{code}:{date}"

    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据"""
        if not self.cache_enabled:
            return None

        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                # 缓存过期，删除
                del self._cache[key]
        return None

    def _set_cache(self, key: str, data: Dict[str, Any]):
        """设置缓存"""
        if self.cache_enabled:
            self._cache[key] = (data, time.time())

    def query_stock_data(self, code: str, date: str) -> Dict[str, Any]:
        """
        查询单只股票的量价数据

        Args:
            code: 股票代码（如 "000001"）
            date: 日期（格式：YYYY-MM-DD）

        Returns:
            包含量价数据的字典

        Raises:
            StockQueryError: 查询失败时抛出
        """
        if self.ak is None:
            raise StockQueryError("akshare 未安装")

        # 检查缓存
        cache_key = self._get_cache_key(code, date)
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data

        try:
            # 查询股票历史数据
            # 注意：AKShare 的接口可能需要根据实际情况调整
            df = self.ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=date.replace("-", ""),
                end_date=date.replace("-", ""),
                adjust="qfq"  # 前复权
            )

            if df.empty:
                raise StockQueryError(f"未找到股票 {code} 在 {date} 的数据")

            # 提取数据
            row = df.iloc[0]
            result = {
                "code": code,
                "date": date,
                "open": float(row.get("开盘", 0)),
                "high": float(row.get("最高", 0)),
                "low": float(row.get("最低", 0)),
                "close": float(row.get("收盘", 0)),
                "volume": float(row.get("成交量", 0)),
                "turnover": float(row.get("成交额", 0)),
                "turnover_rate": float(row.get("换手率", 0)) if "换手率" in row else None,
                "change_pct": float(row.get("涨跌幅", 0)) if "涨跌幅" in row else None,
            }

            # 尝试获取涨停板信息（需要额外接口）
            try:
                result["board_count"] = self._get_board_count(code, date)
                result["is_limit_up"] = abs(result.get("change_pct", 0) - 10.0) < 0.1
            except:
                result["board_count"] = None
                result["is_limit_up"] = None

            # 设置缓存
            self._set_cache(cache_key, result)

            return result

        except Exception as e:
            raise StockQueryError(f"查询股票 {code} 数据失败: {str(e)}")

    def _get_board_count(self, code: str, date: str) -> Optional[int]:
        """
        获取连板数（需要回溯历史数据）

        Args:
            code: 股票代码
            date: 日期

        Returns:
            连板数，如果无法确定则返回 None
        """
        # 这是一个简化实现，实际需要回溯多天数据来计算连板数
        # 这里返回 None，表示需要更复杂的逻辑
        return None

    def batch_query(self, codes: List[str], date: str, max_retries: int = 3) -> Dict[str, Dict[str, Any]]:
        """
        批量查询股票数据

        Args:
            codes: 股票代码列表
            date: 日期（格式：YYYY-MM-DD）
            max_retries: 最大重试次数

        Returns:
            字典，key 为股票代码，value 为量价数据

        Raises:
            StockQueryError: 批量查询失败时抛出
        """
        results = {}
        failed = []

        for code in codes:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    data = self.query_stock_data(code, date)
                    results[code] = data
                    break
                except StockQueryError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        failed.append((code, str(e)))
                    else:
                        # 等待后重试
                        time.sleep(1)

        if failed:
            error_msg = "; ".join([f"{code}: {err}" for code, err in failed])
            raise StockQueryError(f"部分股票查询失败: {error_msg}")

        return results

    def query_limit_up_stocks(self, date: str) -> List[Dict[str, Any]]:
        """
        查询指定日期的涨停板股票

        Args:
            date: 日期（格式：YYYY-MM-DD）

        Returns:
            涨停板股票列表

        Raises:
            StockQueryError: 查询失败时抛出
        """
        if self.ak is None:
            raise StockQueryError("akshare 未安装")

        try:
            # 使用 AKShare 的涨停板接口
            df = self.ak.stock_zt_pool_em(date=date.replace("-", ""))

            if df.empty:
                return []

            results = []
            for _, row in df.iterrows():
                results.append({
                    "code": row.get("代码", ""),
                    "name": row.get("名称", ""),
                    "close": float(row.get("最新价", 0)),
                    "change_pct": float(row.get("涨跌幅", 0)),
                    "turnover_rate": float(row.get("换手率", 0)) if "换手率" in row else None,
                    "volume": float(row.get("成交量", 0)) if "成交量" in row else None,
                    "board_count": int(row.get("连板数", 1)) if "连板数" in row else 1,
                    "first_limit_up_time": row.get("首次封板时间", ""),
                    "last_limit_up_time": row.get("最后封板时间", ""),
                })

            return results

        except Exception as e:
            raise StockQueryError(f"查询涨停板数据失败: {str(e)}")
