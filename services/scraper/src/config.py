"""Configuration for scraper service."""

from shared.config import settings

# Service-specific config (can be overridden)
SCRAPER_ENABLED = settings.scraper_enabled
SCRAPER_TIMEOUT = settings.scraper_timeout_seconds
SCRAPER_RETRY_ATTEMPTS = settings.scraper_retry_attempts
SCRAPER_RETRY_DELAY = settings.scraper_retry_delay_seconds

