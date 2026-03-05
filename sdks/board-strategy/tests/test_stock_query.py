"""
测试 AKShare 查询封装
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from api.stock_query import StockDataQuery, StockQueryError


@pytest.fixture
def mock_akshare():
    """模拟 akshare 模块"""
    with patch('api.stock_query.StockDataQuery.__init__') as mock_init:
        # 让 __init__ 正常执行，但不导入真实的 akshare
        def init_side_effect(self, cache_enabled=True, cache_ttl=3600):
            self.cache_enabled = cache_enabled
            self.cache_ttl = cache_ttl
            self._cache = {}
            self.ak = Mock()  # 使用 Mock 对象代替真实的 akshare

        mock_init.side_effect = init_side_effect
        yield


def test_stock_query_initialization():
    """测试查询器初始化"""
    query = StockDataQuery(cache_enabled=True, cache_ttl=1800)
    assert query.cache_enabled is True
    assert query.cache_ttl == 1800


def test_cache_key_generation():
    """测试缓存键生成"""
    query = StockDataQuery()
    key = query._get_cache_key("000001", "2026-03-03")
    assert key == "000001:2026-03-03"


def test_cache_operations():
    """测试缓存操作"""
    query = StockDataQuery(cache_enabled=True)

    # 设置缓存
    test_data = {"code": "000001", "close": 10.5}
    query._set_cache("test_key", test_data)

    # 获取缓存
    cached = query._get_from_cache("test_key")
    assert cached == test_data

    # 缓存未命中
    not_cached = query._get_from_cache("non_existent_key")
    assert not_cached is None


def test_query_stock_data_without_akshare():
    """测试没有 akshare 时的错误处理"""
    query = StockDataQuery()
    query.ak = None  # 模拟 akshare 未安装

    with pytest.raises(StockQueryError, match="akshare 未安装"):
        query.query_stock_data("000001", "2026-03-03")


def test_batch_query_with_failures():
    """测试批量查询时的失败处理"""
    query = StockDataQuery()

    # 模拟部分成功、部分失败的情况
    def mock_query(code, date):
        if code == "000001":
            return {"code": code, "close": 10.5}
        else:
            raise StockQueryError(f"查询 {code} 失败")

    query.query_stock_data = Mock(side_effect=mock_query)

    # 批量查询应该抛出异常（因为有失败）
    with pytest.raises(StockQueryError, match="部分股票查询失败"):
        query.batch_query(["000001", "000002"], "2026-03-03", max_retries=1)