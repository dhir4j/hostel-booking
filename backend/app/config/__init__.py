"""Configuration selector.

Usage:
    from app.config import get_config
    cfg_cls = get_config()           # reads APP_ENV
    cfg_cls = get_config("testing")  # explicit
"""

from __future__ import annotations

import os
from typing import Optional, Type

from app.config.base import BaseConfig
from app.config.development import DevelopmentConfig
from app.config.production import ProductionConfig
from app.config.testing import TestingConfig

_CONFIG_MAP: dict[str, Type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "testing": TestingConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}


def get_config(env_name: Optional[str] = None) -> Type[BaseConfig]:
    """Return the config class matching ``env_name`` or ``$APP_ENV``.

    Unknown names fall back to :class:`DevelopmentConfig` to keep local boots
    painless; production must set ``APP_ENV=production`` explicitly.
    """
    name = (env_name or os.environ.get("APP_ENV") or "development").lower()
    return _CONFIG_MAP.get(name, DevelopmentConfig)


__all__ = [
    "get_config",
    "BaseConfig",
    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",
]
