#!/bin/bash
# Test the API endpoints to verify the system is working

set -e

API_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing Protego Health Backend API..."
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Check..."
if curl -s -f "${API_URL}/health" > /dev/null; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    curl -s "${API_URL}/health" | python3 -m json.tool
else
    echo -e "${RED}❌ Health check failed - API might not be running${NC}"
    echo "   Run: docker-compose up -d"
    exit 1
fi
echo ""

# Test 2: List Scraping Results
echo "2️⃣  Testing GET /api/v1/scraping..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/v1/scraping?limit=5")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ GET scraping results successful (HTTP $HTTP_CODE)${NC}"
    echo "$BODY" | python3 -m json.tool | head -20
else
    echo -e "${YELLOW}⚠️  GET scraping results returned HTTP $HTTP_CODE${NC}"
    echo "$BODY"
fi
echo ""

# Test 3: List Analysis Results
echo "3️⃣  Testing GET /api/v1/analysis..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/v1/analysis?limit=5")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ GET analysis results successful (HTTP $HTTP_CODE)${NC}"
    echo "$BODY" | python3 -m json.tool | head -20
else
    echo -e "${YELLOW}⚠️  GET analysis results returned HTTP $HTTP_CODE${NC}"
    echo "$BODY"
fi
echo ""

# Test 4: Check OpenAPI Docs
echo "4️⃣  Testing OpenAPI Documentation..."
if curl -s -f "${API_URL}/docs" > /dev/null; then
    echo -e "${GREEN}✅ OpenAPI docs available at ${API_URL}/docs${NC}"
else
    echo -e "${YELLOW}⚠️  OpenAPI docs not accessible${NC}"
fi
echo ""

echo "✅ API Testing Complete!"
echo ""
echo "📚 Next Steps:"
echo "   1. Wait for scraper service to run (runs daily at 2 AM UTC)"
echo "   2. Or manually trigger scraper (if implemented)"
echo "   3. Wait for analysis service to process new data (polls every 5 min)"
echo "   4. Query API endpoints to see scraped and analyzed data"
echo ""

