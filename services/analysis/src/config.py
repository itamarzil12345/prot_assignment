"""Configuration for analysis service."""

from shared.config import settings

# Service-specific config (can be overridden)
ANALYSIS_ENABLED = settings.analysis_enabled
ANALYSIS_POLL_INTERVAL = settings.analysis_poll_interval_seconds
ANALYSIS_BATCH_SIZE = settings.analysis_batch_size

