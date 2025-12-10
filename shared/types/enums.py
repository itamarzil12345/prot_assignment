"""Enumerations for the Protego Health Backend System."""

from enum import Enum


class SourceType(str, Enum):
    """Enumeration for data source types."""

    FDA_DRUG_LABELS = "FDA_DRUG_LABELS"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"


class AnalysisType(str, Enum):
    """Enumeration for analysis result types."""

    KEYWORD_FREQUENCY = "KEYWORD_FREQUENCY"
    CONDITION_GROUPING = "CONDITION_GROUPING"
    CATEGORY_GROUPING = "CATEGORY_GROUPING"


class LogLevel(str, Enum):
    """Enumeration for log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"


class Environment(str, Enum):
    """Enumeration for application environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"

