#!/bin/bash
# Start all Protego Health Backend services

set -e

echo "🚀 Starting Protego Health Backend Services..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Copy .env.example to .env and configure it first:"
    echo "   cp .env.example .env"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create logs directories if they don't exist
mkdir -p services/scraper/logs
mkdir -p services/analysis/logs
mkdir -p services/api/logs

echo "📦 Building and starting all services with Docker Compose..."
echo ""

# Start all services
docker-compose up --build -d

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f              # All services"
echo "   docker-compose logs -f api          # API service only"
echo "   docker-compose logs -f scraper      # Scraper service only"
echo "   docker-compose logs -f analysis     # Analysis service only"
echo ""
echo "🌐 API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "❤️  Health Check:"
echo "   http://localhost:8000/health"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"

