"""Configuration management using Pydantic Settings.

All configuration values come from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from shared.constants import (
    DatabasePool,
    Limits,
    ScheduleCron,
    Timeouts,
)
from shared.types.enums import Environment, LogLevel


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "protego-health-backend"
    app_version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT

    # Database
    database_url: str
    db_pool_size: int = DatabasePool.DEFAULT_SIZE
    db_max_overflow: int = DatabasePool.DEFAULT_MAX_OVERFLOW
    db_pool_timeout: int = DatabasePool.DEFAULT_TIMEOUT
    db_pool_recycle: int = DatabasePool.DEFAULT_RECYCLE

    # Scraper Service
    scraper_schedule_cron: str = ScheduleCron.DAILY_SCRAPER
    scraper_enabled: bool = True
    scraper_timeout_seconds: int = Timeouts.SCRAPER_OPERATION
    scraper_retry_attempts: int = Limits.SCRAPER_RETRY_ATTEMPTS
    scraper_retry_delay_seconds: int = Limits.SCRAPER_RETRY_DELAY

    # Analysis Service
    analysis_enabled: bool = True
    analysis_poll_interval_seconds: int = 300
    analysis_batch_size: int = Limits.ANALYSIS_BATCH_SIZE

    # API Service
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    api_workers: int = 4

    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "json"
    # Log directory is service-specific: services/<service_name>/logs/
    # Not using log_directory from env - each service has its own logs folder
    log_rotation_days: int = Limits.LOG_ROTATION_DAYS
    log_max_bytes: int = Limits.LOG_MAX_BYTES
    log_backup_count: int = Limits.LOG_BACKUP_COUNT

    # HTTP Client
    http_timeout_seconds: int = Timeouts.HTTP_DEFAULT
    http_max_retries: int = 3
    http_retry_delay_seconds: int = 5

    # DailyMed Configuration
    dailymed_base_url: str = "https://dailymed.nlm.nih.gov"

    # Clinical Trials API Configuration
    clinical_trials_api_base_url: str = "https://clinicaltrials.gov/api/v2"
    clinical_trials_api_timeout_seconds: int = Timeouts.HTTP_API


# Global settings instance
settings = Settings()

