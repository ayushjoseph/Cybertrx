"""
Configuration management
Following Single Responsibility Principle (SRP)
"""
import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    echo: bool = False


@dataclass
class APIConfig:
    """External API configuration"""
    nasa_power_url: str
    nasa_power_timeout: int = 30
    max_retries: int = 3


@dataclass
class AppConfig:
    """Application configuration"""
    debug: bool
    host: str
    port: int
    database: DatabaseConfig
    api: APIConfig


class ConfigManager:
    """
    Configuration manager following Single Responsibility Principle.
    Only responsible for loading and providing configuration.
    """
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> AppConfig:
        """Load configuration from environment variables"""
        return AppConfig(
            debug=os.getenv('DEBUG', 'False').lower() == 'true',
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', '8000')),
            database=DatabaseConfig(
                url=os.getenv('DATABASE_URL', 'sqlite:///skyluxe.db'),
                echo=os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
            ),
            api=APIConfig(
                nasa_power_url=os.getenv('NASA_POWER_URL', 'https://power.larc.nasa.gov/api/temporal/daily/point'),
                nasa_power_timeout=int(os.getenv('NASA_POWER_TIMEOUT', '30')),
                max_retries=int(os.getenv('MAX_RETRIES', '3'))
            )
        )
    
    def get_config(self) -> AppConfig:
        """Get the application configuration"""
        return self._config
