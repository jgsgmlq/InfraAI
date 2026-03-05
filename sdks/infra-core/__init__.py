"""
infra-core SDK

AI-Native Infrastructure Framework 核心功能包。
提供工具注册、审查、项目初始化等基础能力。
"""

try:
    from .version import __version__, __version_info__
except ImportError:
    # When running tests directly without package installation
    __version__ = "1.0.0"
    __version_info__ = (1, 0, 0)

__all__ = [
    "__version__",
    "__version_info__",
]
