---
name: Protego Health Backend System
overview: Build a Python/FastAPI-based microservices system with scraper, analysis, and API services for FDA drug labels and clinical trials data, following strict coding standards with repository pattern, strong typing, and Kubernetes orchestration.
todos: []
---

# Protego Health Backend System - Implementation Plan

## Architecture Overview

The system consists of 3 main services (PostgreSQL is remote Neon DB, not a container):

1. **Scraper Service** - Scrapes FDA drug labels and Clinical trials data
2. **Analysis Service** - Analyzes scraped data (keyword mentions, frequency analysis, grouping)
3. **API Service** - Exposes CRUD operations via FastAPI REST API
4. **PostgreSQL** - Remote Neon database (connection string provided, no container needed)

All services communicate via database (read/write to remote Neon PostgreSQL independently).

## Technology Stack

- **Language**: Python 3.11+ with strict type hints and mypy
- **API Framework**: FastAPI
- **Validation**: Pydantic models
- **Database**: PostgreSQL (Neon remote - connection string provided)
- **ORM/Query Builder**: SQLAlchemy (async) + Alembic for migrations
- **Type Checking**: mypy (strict mode)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Communication**: Database-only (no inter-service HTTP calls)
- **HTTP Client**: httpx (for scraping)
- **Testing Framework**: pytest
- **Test Coverage**: pytest-cov, coverage.py
- **HTTP Testing**: httpx (async client), pytest-asyncio
- **Mocking**: pytest-mock, unittest.mock
- **Test Fixtures**: pytest-fixtures, factory-boy (for test data)

## Project Structure

```
protego_task/
├── services/
│   ├── scraper/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── scraper/
│   │   │   │   ├── fda_scraper.py
│   │   │   │   ├── clinical_trials_scraper.py
│   │   │   │   └── scraper_interface.py
│   │   │   ├── repository/
│   │   │   │   ├── scraping_repository.py
│   │   │   │   └── scraping_repository_interface.py
│   │   │   ├── models/
│   │   │   │   ├── scraping_result_model.py
│   │   │   │   └── scraping_result_dto.py
│   │   │   ├── scheduler/
│   │   │   │   └── daily_scheduler.py
│   │   │   ├── errors/
│   │   │   │   └── scraper_errors.py
│   │   │   ├── logging/
│   │   │   │   └── service_logger.py (wrapper for shared logger)
│   │   │   ├── constants.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   ├── analysis/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── analyzer/
│   │   │   │   ├── keyword_analyzer.py
│   │   │   │   ├── frequency_analyzer.py
│   │   │   │   └── analyzer_interface.py
│   │   │   ├── repository/
│   │   │   │   ├── analysis_repository.py
│   │   │   │   └── analysis_repository_interface.py
│   │   │   ├── models/
│   │   │   │   ├── analysis_result_model.py
│   │   │   │   └── analysis_result_dto.py
│   │   │   ├── scheduler/
│   │   │   │   └── analysis_scheduler.py
│   │   │   ├── errors/
│   │   │   │   └── analysis_errors.py
│   │   │   ├── logging/
│   │   │   │   └── service_logger.py (wrapper for shared logger)
│   │   │   ├── constants.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   └── api/
│       ├── src/
│       │   ├── main.py
│       │   ├── routes/
│       │   │   ├── scraping_routes.py
│       │   │   ├── analysis_routes.py
│       │   │   └── __init__.py
│       │   ├── handlers/
│       │   │   ├── scraping_handler.py
│       │   │   └── analysis_handler.py
│       │   ├── repository/
│       │   │   ├── scraping_repository.py
│       │   │   ├── analysis_repository.py
│       │   │   └── *.repository_interface.py
│       │   ├── models/
│       │   │   ├── *.model.py
│       │   │   ├── *.dto.py (Pydantic)
│       │   │   └── *.schema.py (Pydantic)
│       │   ├── middleware/
│       │   │   ├── error_handler.py
│       │   │   └── validation_middleware.py
│       │   ├── errors/
│       │   │   └── api_errors.py
│       │   ├── database/
│       │   │   ├── base.py (SQLAlchemy base)
│       │   │   ├── session.py
│       │   │   └── models.py (ORM models)
│       │   ├── logging/
│       │   │   └── service_logger.py (wrapper for shared logger)
│       │   ├── constants.py
│       │   └── config.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── pyproject.toml
├── shared/
│   ├── types/
│   │   ├── enums.py
│   │   └── common_types.py
│   ├── logging/
│   │   ├── logger_factory.py
│   │   ├── logger_interface.py
│   │   ├── log_formatter.py
│   │   └── log_handlers.py
│   ├── constants.py
│   └── config.py
├── logs/
│   ├── scraper/
│   │   ├── error.log
│   │   ├── info.log
│   │   ├── debug.log
│   │   ├── warning.log
│   │   └── audit.log
│   ├── analysis/
│   │   ├── error.log
│   │   ├── info.log
│   │   ├── debug.log
│   │   ├── warning.log
│   │   └── audit.log
│   └── api/
│       ├── error.log
│       ├── info.log
│       ├── debug.log
│       ├── warning.log
│       └── audit.log
├── migrations/
│   └── alembic/
│       ├── versions/
│       └── env.py
├── tests/
│   ├── scraper/
│   │   ├── unit/
│   │   │   ├── test_fda_scraper.py
│   │   │   ├── test_clinical_trials_scraper.py
│   │   │   ├── test_scraper_factory.py
│   │   │   ├── test_daily_scheduler.py
│   │   │   └── test_scraping_repository.py
│   │   ├── integration/
│   │   │   ├── test_scraper_integration.py
│   │   │   └── test_repository_integration.py
│   │   ├── fixtures/
│   │   │   └── scraper_fixtures.py
│   │   └── conftest.py
│   ├── analysis/
│   │   ├── unit/
│   │   │   ├── test_keyword_analyzer.py
│   │   │   ├── test_frequency_analyzer.py
│   │   │   ├── test_analysis_strategy.py
│   │   │   ├── test_analysis_repository.py
│   │   │   └── test_analysis_scheduler.py
│   │   ├── integration/
│   │   │   ├── test_analyzer_integration.py
│   │   │   └── test_analysis_repository_integration.py
│   │   ├── fixtures/
│   │   │   └── analysis_fixtures.py
│   │   └── conftest.py
│   ├── api/
│   │   ├── unit/
│   │   │   ├── test_scraping_handler.py
│   │   │   ├── test_analysis_handler.py
│   │   │   ├── test_middleware.py
│   │   │   ├── test_validation.py
│   │   │   └── test_error_handler.py
│   │   ├── integration/
│   │   │   ├── test_scraping_routes.py
│   │   │   ├── test_analysis_routes.py
│   │   │   └── test_api_integration.py
│   │   ├── fixtures/
│   │   │   └── api_fixtures.py
│   │   └── conftest.py
│   ├── shared/
│   │   ├── test_logger.py
│   │   ├── test_logger_factory.py
│   │   └── test_utils.py
│   └── conftest.py
├── k8s/
│   ├── scraper-deployment.yaml
│   ├── analysis-deployment.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   └── configmap.yaml (for config)
├── docker-compose.yml (for local dev - no postgres container)
├── .env.example
├── pyproject.toml (root)
├── mypy.ini
├── pytest.ini
└── README.md
```

## Database Schema

**Tables:**

- `scraping_results` - Raw scraped data
  - id (UUID), source_type (enum), external_id (str), title (str), data (JSONB), link (str), scraped_at (timestamp)
- `analysis_results` - Analyzed data
  - id (UUID), scraping_result_id (UUID, FK), analysis_type (enum), keyword (str), frequency (int), metadata (JSONB), created_at (timestamp)

## Key Implementation Details

### 1. Constants & Configuration

- All string literals in `constants.py` files
- All config values in `config.py` (env vars, timeouts, thresholds)
- Enums (`Enum` from `enum` module) for source types, analysis types, error codes
- Table names, route paths, error messages as constants

### 2. Repository Pattern

- Abstract base classes (`ABC`) for repository interfaces
- Separate repository files per entity
- SQLAlchemy async for database queries
- Each repository < 300 lines

### 3. Type Safety (Python)

- Type hints everywhere (`typing` module)
- mypy strict mode configuration
- Pydantic models for validation and DTOs
- TypedDict for structured dictionaries
- No bare types, use `Optional`, `Union`, `List`, `Dict` from typing
- Use `Protocol` for structural typing when needed

### 4. Error Handling

- Typed exception classes inheriting from custom base exceptions
- Error codes as constants/enums
- Centralized error mapping
- No bare `raise Exception("string")` - always use typed exceptions

### 5. Service Responsibilities

**Scraper Service:**

- Scrapes FDA drug labels from dailymed.nlm.nih.gov (using httpx)
- Scrapes Clinical trials from clinicaltrials.gov (using httpx)
- Saves raw data to `scraping_results` table via repository
- Runs once per day on scheduled interval (configurable via cron expression, default: daily at 2 AM UTC)
- Manual trigger capability via database flag or API endpoint for testing

**Analysis Service:**

- Reads from `scraping_results` table via repository
- Performs keyword frequency analysis
- Groups by condition/category
- Saves results to `analysis_results` table via repository
- Runs periodically on new/unprocessed data

**API Service:**

- FastAPI app with OpenAPI/Swagger docs
- CRUD operations for scraping results
- CRUD operations for analysis results
- Pydantic models for request/response validation
- Error handling middleware
- Connects to remote Neon PostgreSQL

### 6. File Size Management

- Aggressive splitting: each handler < 150 lines
- Separate files for routes, handlers, repositories
- Extract utilities to separate modules
- Keep models/DTOs in separate files

### 7. Logging System

- Centralized logging infrastructure using Factory pattern
- Each service maintains at least 5 log files in `services/<service_name>/logs/`:
  - `error.log` - Error level logs only
  - `info.log` - Info level logs (operational events)
  - `debug.log` - Debug level logs (detailed debugging info)
  - `warning.log` - Warning level logs
  - `audit.log` - Audit trail logs (security, access, data changes)
- Logger interface for dependency inversion
- Structured logging with JSON format for production
- Log rotation configured (daily rotation, keep 30 days)
- Log levels configurable per environment
- Service name, timestamp, correlation ID in every log entry

### 8. Design Patterns & Architecture

**Required Design Patterns:**

1. **Factory Pattern** - For creating scrapers, analyzers, loggers
2. **Strategy Pattern** - For different scraping strategies, analysis algorithms
3. **Repository Pattern** - Data access abstraction (already specified)
4. **Dependency Injection** - Via ABC interfaces and DI container
5. **Builder Pattern** - For complex query construction, configuration objects
6. **Adapter Pattern** - For external API integrations, data transformations
7. **Decorator Pattern** - For middleware, validation, caching, logging decorators
8. **Observer Pattern** - For event-driven logging, metrics collection
9. **Singleton Pattern** - For database connection pools, configuration managers (careful use)
10. **Command Pattern** - For scheduled tasks, operation queuing
11. **Template Method Pattern** - For scraping workflows, analysis pipelines
12. **Facade Pattern** - For complex subsystem interfaces

**Clean Architecture Layers:**

- **Domain Layer**: Business entities, value objects, domain services, interfaces
- **Application Layer**: Use cases, DTOs, application services, interfaces
- **Infrastructure Layer**: Repository implementations, external service adapters, database
- **Presentation Layer**: API handlers, routes, middleware (FastAPI)

**SOLID Principles Strict Enforcement:**

- **Single Responsibility**: Each class/module has ONE reason to change
- **Open/Closed**: Open for extension, closed for modification (use interfaces, inheritance)
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Small, focused interfaces (no fat interfaces)
- **Dependency Inversion**: Depend on abstractions (interfaces), not concretions

**Additional Guidelines:**

- **DRY (Don't Repeat Yourself)**: Extract common functionality
- **KISS (Keep It Simple, Stupid)**: Prefer simple solutions
- **YAGNI (You Aren't Gonna Need It)**: Don't over-engineer
- **Composition over Inheritance**: Prefer composition
- **Favor Immutability**: Use immutable data structures where possible
- **Fail Fast**: Validate inputs early, raise exceptions immediately
- **Explicit over Implicit**: Make dependencies and flows explicit

## Data Flow

1. **Scraping Flow:**

   - Scraper service runs once daily on scheduled interval (configurable, default 2 AM UTC)
   - Manual trigger available via database flag for testing
   - Factory pattern creates appropriate scraper (FDA or Clinical Trials)
   - Fetches data from FDA/Clinical trials APIs (httpx)
   - Logs all operations to appropriate log files (info, debug, error, audit)
   - Validates and transforms data using Pydantic models
   - Saves to `scraping_results` via repository (SQLAlchemy async)
   - Logs completion status and metrics

2. **Analysis Flow:**

   - Analysis service polls for new/unprocessed scraping results
   - Performs keyword extraction and frequency analysis
   - Groups data by conditions/categories
   - Saves results to `analysis_results` via repository

3. **API Flow:**
   - Client makes request to FastAPI service
   - Middleware logs request (audit log), adds correlation ID
   - Route handler validates input (Pydantic decorator pattern)
   - Handler calls repository (dependency injection)
   - Repository queries remote Neon database (SQLAlchemy async)
   - Logs query execution (debug log)
   - Pydantic response model returned to client
   - Middleware logs response (audit log)
   - Error handling middleware catches exceptions, logs to error log

## Python-Specific Implementation

### Type Checking

```python
# mypy.ini - strict mode
[mypy]
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
```

### Logging Architecture

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"

class LoggerInterface(ABC):
    @abstractmethod
    async def error(self, message: str, correlation_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def info(self, message: str, correlation_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def debug(self, message: str, correlation_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def warning(self, message: str, correlation_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def audit(self, message: str, correlation_id: Optional[str] = None) -> None:
        pass

# Logger Factory Pattern
class LoggerFactory:
    @staticmethod
    def create_logger(service_name: str) -> LoggerInterface:
        # Returns configured logger instance
        pass
```

### Design Pattern Examples

**Factory Pattern for Scrapers:**

```python
from abc import ABC, abstractmethod
from enum import Enum

class SourceType(str, Enum):
    FDA_DRUG_LABELS = "FDA_DRUG_LABELS"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"

class ScraperInterface(ABC):
    @abstractmethod
    async def scrape(self) -> list[ScrapingResultDTO]:
        pass

class ScraperFactory:
    @staticmethod
    def create(source_type: SourceType) -> ScraperInterface:
        if source_type == SourceType.FDA_DRUG_LABELS:
            return FDAScraper()
        elif source_type == SourceType.CLINICAL_TRIALS:
            return ClinicalTrialsScraper()
        raise ValueError(f"Unknown source type: {source_type}")
```

**Strategy Pattern for Analysis:**

```python
class AnalysisStrategy(ABC):
    @abstractmethod
    async def analyze(self, data: ScrapingResultDTO) -> AnalysisResultDTO:
        pass

class KeywordFrequencyStrategy(AnalysisStrategy):
    async def analyze(self, data: ScrapingResultDTO) -> AnalysisResultDTO:
        # Implementation
        pass

class ConditionGroupingStrategy(AnalysisStrategy):
    async def analyze(self, data: ScrapingResultDTO) -> AnalysisResultDTO:
        # Implementation
        pass
```

**Builder Pattern for Complex Queries:**

```python
class QueryBuilder:
    def __init__(self) -> None:
        self._conditions: list[str] = []
        self._joins: list[str] = []

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def join(self, table: str, on: str) -> "QueryBuilder":
        self._joins.append(f"JOIN {table} ON {on}")
        return self

    def build(self) -> str:
        # Construct SQL query
        pass
```

### Pydantic Models Example

```python
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class SourceType(str, Enum):
    FDA_DRUG_LABELS = "FDA_DRUG_LABELS"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"

class ScrapingResultDTO(BaseModel):
    id: str
    source_type: SourceType
    external_id: str
    title: str
    data: dict[str, Any]
    link: str
    scraped_at: datetime
```

### Repository Pattern (ABC)

```python
from abc import ABC, abstractmethod
from typing import Optional

class ScrapingRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, result: ScrapingResultDTO) -> str:
        pass

    @abstractmethod
    async def get_by_id(self, result_id: str) -> Optional[ScrapingResultDTO]:
        pass
```

## Kubernetes Configuration

- 3 deployments: scraper, analysis, api
- 1 service: api (for external access)
- ConfigMap for shared configuration (excluding DB credentials)
- Secrets for database connection string
- No PostgreSQL deployment (using remote Neon DB)

## Implementation Steps

1. **Setup project structure** - Initialize Python project with pyproject.toml, mypy config, logging structure
2. **Shared types & constants** - Enums, common constants, type definitions
3. **Logging infrastructure** - Logger factory, interfaces, handlers, formatters for all log types
4. **Database setup** - SQLAlchemy models, Alembic migrations for remote Neon DB
5. **Design pattern foundations** - Factory, Strategy, Builder, Adapter base classes
6. **Repository layer** - ABC-based repositories for all services
7. **Scraper service** - Implement FDA and Clinical trials scrapers with httpx (Factory pattern)
8. **Scheduler implementation** - Daily cron scheduler for scraper service
9. **Analysis service** - Keyword and frequency analyzers (Strategy pattern)
10. **API service** - FastAPI setup with routes, handlers, OpenAPI docs, middleware
11. **Error handling** - Typed exception classes and centralized error mapping
12. **Dependency Injection** - DI container setup for service composition
13. **Test infrastructure** - Set up pytest, fixtures, test factories, mocking utilities
14. **Unit tests** - Write comprehensive unit tests for all services (80%+ coverage)
15. **Integration tests** - Write integration tests for repositories and external services
16. **Docker configuration** - Dockerfiles for each service (no postgres container), log volume mounts
17. **Kubernetes manifests** - Deployments and services (no postgres), log volume persistence
18. **CI/CD pipeline** - Configure test execution, coverage reporting, quality gates
19. **Documentation** - README with architecture diagram, design patterns, testing guide, and setup instructions

## Design Trade-offs

1. **Database-only communication**: Simpler than message queues, but tighter coupling to DB schema
2. **Remote Neon DB**: No local DB container needed, but requires internet and connection management
3. **Polling vs Events**: Analysis service polls DB - simple but less efficient than events
4. **Monorepo structure**: Easier code sharing, but requires careful dependency management
5. **SQLAlchemy async**: Mature ORM with good type hints, but requires async/await throughout codebase

## Strict Software Engineering Standards

### Code Quality Requirements

1. **Type Safety**

   - Every function must have complete type hints
   - No `Any` types allowed (use `Unknown` if type is truly unknown)
   - Use `TypedDict` for dictionaries with known structure
   - Use `Protocol` for structural typing
   - All return types must be explicit, no implicit `None`

2. **Documentation**

   - All public classes, methods, functions must have docstrings (Google style)
   - Complex logic must have inline comments explaining WHY, not WHAT
   - README files in each service directory explaining service purpose

3. **Testing Standards** - See comprehensive "Testing & Coverage Requirements" section below

4. **Code Organization**

   - Maximum 300 lines per file (strictly enforced)
   - One class per file (exceptions: related value objects, exceptions)
   - Group related functions into modules
   - Clear separation of concerns across layers

5. **Error Handling**

   - Custom exception hierarchy with base exception classes
   - Exception context propagation (use exception chaining)
   - Never swallow exceptions silently (log and re-raise or handle)
   - Specific exception types for different error scenarios

6. **Performance**

   - Async/await for all I/O operations (database, HTTP requests)
   - Connection pooling for database connections
   - Timeout configurations for all external calls
   - Resource cleanup in `finally` blocks or context managers

7. **Security**

   - Never log sensitive data (passwords, tokens, PII)
   - Input validation at API boundaries
   - SQL injection prevention (use parameterized queries)
   - Environment variables for all secrets (never hardcode)

8. **Configuration Management**
   - All configuration via environment variables
   - Type-safe configuration classes (Pydantic Settings)
   - Configuration validation on startup
   - Default values for non-critical settings

### Design Pattern Enforcement

**Mandatory Patterns:**

- **Factory**: All object creation (scrapers, analyzers, loggers, repositories)
- **Strategy**: All algorithms with multiple implementations (analysis types)
- **Repository**: All data access (database operations)
- **Dependency Injection**: All service dependencies (via constructor injection)
- **Decorator**: Cross-cutting concerns (logging, validation, caching)
- **Builder**: Complex object construction (queries, configuration)

**Optional Patterns (Use When Appropriate):**

- **Observer**: Event-driven logging, metrics
- **Command**: Scheduled tasks, operation queuing
- **Template Method**: Workflow definitions
- **Facade**: Complex subsystem interfaces
- **Adapter**: External service integrations

### Clean Architecture Layers

```
┌─────────────────────────────────────┐
│     Presentation Layer (FastAPI)    │
│  Routes → Handlers → Middleware     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Application Layer              │
│  Use Cases → DTOs → Validators      │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│        Domain Layer                 │
│  Entities → Value Objects → Domain  │
│  Services → Interfaces              │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     Infrastructure Layer            │
│  Repositories → External Services   │
│  Database → HTTP Clients            │
└─────────────────────────────────────┘
```

**Layer Rules:**

- Dependencies flow inward (outer layers depend on inner)
- Inner layers define interfaces, outer layers implement
- Domain layer has no external dependencies
- Infrastructure layer implements domain interfaces

### Dependency Injection Container

```python
# Container pattern for managing dependencies
class DIContainer:
    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, interface: type, implementation: type) -> None:
        self._services[interface.__name__] = implementation

    def resolve(self, interface: type) -> Any:
        # Returns configured instance
        pass
```

## Constants Examples

```python
# constants.py
from enum import Enum

class SourceType(str, Enum):
    FDA_DRUG_LABELS = "FDA_DRUG_LABELS"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"

class AnalysisType(str, Enum):
    KEYWORD_FREQUENCY = "KEYWORD_FREQUENCY"
    CONDITION_GROUPING = "CONDITION_GROUPING"

class Tables:
    SCRAPING_RESULTS = "scraping_results"
    ANALYSIS_RESULTS = "analysis_results"

class Routes:
    SCRAPING = "/api/v1/scraping"
    ANALYSIS = "/api/v1/analysis"

class LogFiles:
    ERROR = "error.log"
    INFO = "info.log"
    DEBUG = "debug.log"
    WARNING = "warning.log"
    AUDIT = "audit.log"

class ScheduleCron:
    DAILY_SCRAPER = "0 2 * * *"  # Daily at 2 AM UTC
```

## Testing & Coverage Requirements

### Coverage Requirements

**Mandatory Coverage Targets:**

- **Minimum 80% overall code coverage** for each service
- **Minimum 90% coverage** for business logic (scrapers, analyzers, handlers)
- **Minimum 85% coverage** for repository implementations
- **100% coverage** for error handling paths
- **100% coverage** for validation logic
- Coverage reports generated in HTML and XML formats
- Coverage enforcement in CI/CD pipeline (fails build if below threshold)

### Testing Framework & Tools

- **pytest** - Primary testing framework
- **pytest-asyncio** - Async test support
- **pytest-cov** - Coverage plugin
- **pytest-mock** - Mocking utilities
- **httpx** - Async HTTP client for API testing
- **factory-boy** - Test data factories
- **faker** - Fake data generation
- **pytest-xdist** - Parallel test execution
- **pytest-timeout** - Test timeout management

### Test Structure Per Service

#### Scraper Service Tests

**Unit Tests:**

- `test_fda_scraper.py` - Test FDA scraper logic, data parsing, error handling
- `test_clinical_trials_scraper.py` - Test clinical trials scraper logic
- `test_scraper_factory.py` - Test Factory pattern for scraper creation
- `test_daily_scheduler.py` - Test scheduler cron execution, manual triggers
- `test_scraping_repository.py` - Test repository methods (mocked DB)

**Integration Tests:**

- `test_scraper_integration.py` - End-to-end scraping with mocked HTTP responses
- `test_repository_integration.py` - Database integration with test DB

**Test Scenarios:**

- Successful scraping from FDA API
- Successful scraping from Clinical Trials API
- HTTP error handling (timeouts, 404, 500)
- Data validation and transformation
- Duplicate detection
- Scheduler execution at correct intervals
- Manual trigger functionality
- Error logging and recovery

#### Analysis Service Tests

**Unit Tests:**

- `test_keyword_analyzer.py` - Keyword extraction algorithms
- `test_frequency_analyzer.py` - Frequency counting logic
- `test_analysis_strategy.py` - Strategy pattern implementation
- `test_analysis_repository.py` - Repository methods (mocked DB)
- `test_analysis_scheduler.py` - Scheduler polling logic

**Integration Tests:**

- `test_analyzer_integration.py` - Full analysis pipeline with test data
- `test_analysis_repository_integration.py` - Database integration

**Test Scenarios:**

- Keyword frequency calculation accuracy
- Condition grouping correctness
- Analysis of various data formats
- Handling missing/invalid data
- Batch processing multiple scraping results
- Strategy switching and execution
- Performance with large datasets

#### API Service Tests

**Unit Tests:**

- `test_scraping_handler.py` - Handler logic, error handling
- `test_analysis_handler.py` - Handler logic, error handling
- `test_middleware.py` - Middleware functionality (logging, correlation IDs)
- `test_validation.py` - Pydantic model validation
- `test_error_handler.py` - Error mapping and responses

**Integration Tests:**

- `test_scraping_routes.py` - CRUD operations for scraping results
- `test_analysis_routes.py` - CRUD operations for analysis results
- `test_api_integration.py` - Full API request/response cycles

**Test Scenarios:**

- GET requests (single item, list, pagination)
- POST requests (create operations, validation)
- PUT/PATCH requests (update operations)
- DELETE requests
- Error responses (404, 400, 500)
- Authentication/authorization (if implemented)
- Request validation failures
- Database connection errors
- Middleware execution order
- Audit logging of API calls

#### Shared Components Tests

**Tests:**

- `test_logger.py` - Logger functionality, log levels, formatting
- `test_logger_factory.py` - Factory pattern for logger creation
- `test_utils.py` - Utility functions, helpers

### Test Data Management

**Fixtures & Factories:**

- Use `factory-boy` for creating test data models
- Centralized fixture files per service (`conftest.py`)
- Reusable fixtures for database sessions, HTTP clients, loggers
- Mock external APIs using `pytest-httpx` or `responses`
- Test database setup/teardown in fixtures

**Test Data Examples:**

```python
# Using factory-boy
class ScrapingResultFactory(factory.Factory):
    class Meta:
        model = ScrapingResultDTO

    id = factory.Faker('uuid4')
    source_type = SourceType.FDA_DRUG_LABELS
    title = factory.Faker('sentence')
    # ... other fields
```

### Mocking Strategy

**External Dependencies:**

- Mock HTTP requests to FDA/Clinical Trials APIs using `pytest-httpx`
- Mock database connections for unit tests
- Mock logger for isolated testing
- Mock scheduler for time-based tests

**Repository Tests:**

- Use in-memory SQLite for integration tests
- Mock SQLAlchemy sessions for unit tests
- Test query builders separately

### Test Execution

**Local Execution:**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov-report=html --cov-report=term

# Run specific service tests
pytest tests/scraper/
pytest tests/analysis/
pytest tests/api/

# Run specific test file
pytest tests/scraper/unit/test_fda_scraper.py

# Run in parallel
pytest -n auto
```

**CI/CD Integration:**

- Tests run on every commit/pull request
- Coverage report uploaded as artifact
- Build fails if coverage below 80%
- Coverage badge in README

### Test Configuration

**pytest.ini:**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts =
    --strict-markers
    --cov=services
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
    -v
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Test Quality Standards

1. **Test Naming**: Descriptive names following pattern `test_<what>_<condition>_<expected_result>`
2. **AAA Pattern**: Arrange, Act, Assert structure
3. **Test Isolation**: Each test must be independent, no shared state
4. **Clean Setup/Teardown**: Use fixtures for setup, ensure proper cleanup
5. **Assertions**: Specific assertions, not just `assert True`
6. **Test Documentation**: Docstrings explaining what is being tested
7. **Edge Cases**: Test boundary conditions, error cases, null values
8. **Performance**: Tests should run quickly (< 1 second per test ideally)

### Test Coverage Reports

**Generated Reports:**

- HTML coverage report (`htmlcov/index.html`)
- XML coverage report (for CI/CD integration)
- Terminal output with missing lines
- Coverage badges (via services like codecov.io)

**Coverage Exclusions:**

- Migration files
- Configuration files
- `__main__` blocks
- Type checking ignores (`# type: ignore` lines)

## Scheduler Configuration

**Scraper Service Schedule:**

- Default: Runs once per day at 2 AM UTC (configurable via `SCRAPER_SCHEDULE_CRON` env var)
- Cron expression format: `"0 2 * * *"` (minute hour day month weekday)
- Scheduler implementation uses `APScheduler` or similar
- Failure handling: Log errors, retry logic configurable
- Manual override: Database flag or API endpoint for immediate execution
