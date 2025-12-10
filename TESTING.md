# Testing Guide

## Quick Start - Full System Test

### 1. Start All Services
```bash
# Option 1: Using the convenience script
./scripts/start.sh

# Option 2: Using docker-compose directly
docker-compose up --build -d
```

This starts all three services in parallel:
- **Scraper Service** - Runs on schedule (default: 2 AM UTC daily)
- **Analysis Service** - Polls for unprocessed data every 5 minutes
- **API Service** - Available at http://localhost:8000

### 2. Verify Services Are Running
```bash
# Check service status
docker-compose ps

# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f scraper
docker-compose logs -f analysis
```

### 3. Test API Endpoints
```bash
# Option 1: Use the test script
./scripts/test-api.sh

# Option 2: Manual testing
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/scraping
curl http://localhost:8000/api/v1/analysis

# Option 3: Use Postman (MCP available)
# Open API docs at http://localhost:8000/docs
```

## Testing Workflow

### Initial State (No Data)
1. Services start successfully ✅
2. Health check returns `{"status": "healthy", "service": "protego-health-api"}` ✅
3. API endpoints return empty lists (no data yet) ✅

### After Scraper Runs (Once Daily)
1. Scraper fetches data from FDA DailyMed and ClinicalTrials.gov
2. Data saved to `scraping_results` table
3. Check logs: `docker-compose logs scraper`
4. Verify data: `curl http://localhost:8000/api/v1/scraping`

### After Analysis Processes Data (Every 5 Minutes)
1. Analysis service finds unprocessed scraping results
2. Performs keyword frequency and condition grouping analysis
3. Saves results to `analysis_results` table
4. Check logs: `docker-compose logs analysis`
5. Verify data: `curl http://localhost:8000/api/v1/analysis`

## Manual Testing Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### List Scraping Results
```bash
# Get all scraping results (paginated)
curl "http://localhost:8000/api/v1/scraping?limit=10&offset=0"

# Filter by source type
curl "http://localhost:8000/api/v1/scraping?source_type=FDA_DRUG_LABELS"

# Get specific result
curl http://localhost:8000/api/v1/scraping/{result_id}
```

### List Analysis Results
```bash
# Get all analysis results
curl "http://localhost:8000/api/v1/analysis?limit=10&offset=0"

# Filter by analysis type
curl "http://localhost:8000/api/v1/analysis?analysis_type=KEYWORD_FREQUENCY"

# Filter by scraping result ID
curl "http://localhost:8000/api/v1/analysis?scraping_result_id={uuid}"

# Get specific result
curl http://localhost:8000/api/v1/analysis/{result_id}
```

### Update Operations
```bash
# Update scraping result
curl -X PUT http://localhost:8000/api/v1/scraping/{result_id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Update analysis result
curl -X PUT http://localhost:8000/api/v1/analysis/{result_id} \
  -H "Content-Type: application/json" \
  -d '{"frequency": 42}'
```

### Delete Operations
```bash
# Delete scraping result
curl -X DELETE http://localhost:8000/api/v1/scraping/{result_id}

# Delete analysis result
curl -X DELETE http://localhost:8000/api/v1/analysis/{result_id}
```

## Testing Individual Services

### Test Scraper Service
```bash
# View scraper logs
docker-compose logs -f scraper

# Check scraper logs directory
ls -la services/scraper/logs/

# Verify scraper created data
curl "http://localhost:8000/api/v1/scraping?source_type=FDA_DRUG_LABELS"
```

### Test Analysis Service
```bash
# View analysis logs
docker-compose logs -f analysis

# Check analysis logs directory
ls -la services/analysis/logs/

# Verify analysis created results
curl "http://localhost:8000/api/v1/analysis?analysis_type=KEYWORD_FREQUENCY"
```

### Test API Service
```bash
# View API logs
docker-compose logs -f api

# Check API logs directory
ls -la services/api/logs/

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/scraping
```

## Testing Database Connection

```bash
# Connect to database using connection string from .env
psql "${DATABASE_URL}"

# Check tables exist
\dt

# Check scraping results
SELECT COUNT(*) FROM scraping_results;

# Check analysis results
SELECT COUNT(*) FROM analysis_results;

# View recent scraping results
SELECT id, source_type, title, scraped_at 
FROM scraping_results 
ORDER BY scraped_at DESC 
LIMIT 10;
```

## Troubleshooting

### Services won't start
1. Check `.env` file exists and has correct `DATABASE_URL`
2. Verify database is accessible: `psql "${DATABASE_URL}"`
3. Check logs: `docker-compose logs`

### No data in API responses
1. Scraper runs once daily at 2 AM UTC (or configured time)
2. Wait for next scheduled run, or check scraper logs for errors
3. Verify database connection from scraper service

### Analysis not processing data
1. Analysis polls every 5 minutes (configurable)
2. Check analysis logs for errors
3. Verify scraping results exist in database
4. Check that analysis service can connect to database

### API errors
1. Check API logs: `docker-compose logs api`
2. Verify database connection
3. Check request format matches API schema (see `/docs`)

## Automated Testing (TODO)

Unit tests, integration tests, and test coverage will be added in a future update. See `pytest.ini` for configuration.

