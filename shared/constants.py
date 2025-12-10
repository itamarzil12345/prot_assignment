"""Constants for the Protego Health Backend System.

All string literals and magic numbers must be defined here.
"""


class Tables:
    """Database table names."""

    SCRAPING_RESULTS = "scraping_results"
    ANALYSIS_RESULTS = "analysis_results"


class Routes:
    """API route paths."""

    SCRAPING = "/api/v1/scraping"
    ANALYSIS = "/api/v1/analysis"
    HEALTH = "/health"


class LogFiles:
    """Log file names."""

    ERROR = "error.log"
    INFO = "info.log"
    DEBUG = "debug.log"
    WARNING = "warning.log"
    AUDIT = "audit.log"


class ScheduleCron:
    """Cron schedule expressions."""

    DAILY_SCRAPER = "0 2 * * *"  # Daily at 2 AM UTC


class ErrorMessages:
    """Error messages as constants."""

    DATABASE_CONNECTION_ERROR = "Failed to connect to database"
    SCRAPING_ERROR = "Failed to scrape data from source"
    ANALYSIS_ERROR = "Failed to analyze data"
    NOT_FOUND = "Resource not found"
    VALIDATION_ERROR = "Validation failed"
    INTERNAL_SERVER_ERROR = "Internal server error"


class Timeouts:
    """Timeout values in seconds."""

    HTTP_DEFAULT = 30
    HTTP_API = 60
    DATABASE_QUERY = 30
    SCRAPER_OPERATION = 300


class Limits:
    """System limits and thresholds."""

    ANALYSIS_BATCH_SIZE = 100
    ANALYSIS_KEYWORD_LIMIT = 50  # Maximum keywords per analysis result
    MIN_KEYWORD_LENGTH = 3  # Minimum word length for keyword extraction
    MAX_KEYWORD_FREQUENCY_RESULTS = 50  # Max keywords per analysis result
    SCRAPER_RETRY_ATTEMPTS = 3
    SCRAPER_RETRY_DELAY = 60
    LOG_MAX_BYTES = 10485760  # 10 MB
    LOG_BACKUP_COUNT = 5
    LOG_ROTATION_DAYS = 30


class DatabasePool:
    """Database connection pool settings."""

    DEFAULT_SIZE = 20
    DEFAULT_MAX_OVERFLOW = 10
    DEFAULT_TIMEOUT = 30
    DEFAULT_RECYCLE = 3600

