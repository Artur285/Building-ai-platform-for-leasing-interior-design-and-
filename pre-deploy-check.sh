#!/bin/bash
# Pre-deployment checklist script

echo "🚀 AI Building Materials Leasing Platform - Pre-Deployment Checklist"
echo "=================================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check_item() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        return 1
    fi
}

FAILED=0

# Check 1: Environment file exists
echo "1. Checking environment configuration..."
if [ -f ".env" ]; then
    check_item 0 ".env file exists"
else
    check_item 1 ".env file missing - copy from .env.example"
    FAILED=1
fi
echo ""

# Check 2: Dependencies
echo "2. Checking dependencies..."
if [ -f "requirements.txt" ]; then
    check_item 0 "requirements.txt exists"
else
    check_item 1 "requirements.txt missing"
    FAILED=1
fi
echo ""

# Check 3: Docker
echo "3. Checking Docker..."
if command -v docker &> /dev/null; then
    check_item 0 "Docker is installed"
    if docker ps &> /dev/null; then
        check_item 0 "Docker daemon is running"
    else
        check_item 1 "Docker daemon is not running"
        FAILED=1
    fi
else
    check_item 1 "Docker is not installed"
    FAILED=1
fi
echo ""

# Check 4: Docker Compose
echo "4. Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    check_item 0 "Docker Compose is installed"
else
    check_item 1 "Docker Compose is not installed"
    FAILED=1
fi
echo ""

# Check 5: Configuration files
echo "5. Checking configuration files..."
FILES=("config.py" "gunicorn_config.py" "docker-compose.prod.yml" "Dockerfile" "nginx.conf")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        check_item 0 "$file exists"
    else
        check_item 1 "$file missing"
        FAILED=1
    fi
done
echo ""

# Check 6: Directory structure
echo "6. Checking directory structure..."
DIRS=("app" "static" "data" "logs")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ] || [ "$dir" == "data" ] || [ "$dir" == "logs" ]; then
        if [ "$dir" == "data" ] || [ "$dir" == "logs" ]; then
            mkdir -p "$dir" 2>/dev/null
        fi
        check_item 0 "$dir directory ready"
    else
        check_item 1 "$dir directory missing"
        FAILED=1
    fi
done
echo ""

# Check 7: Security
echo "7. Checking security configuration..."
if [ -f ".env" ]; then
    if grep -q "SECRET_KEY=your-secret-key-here" .env 2>/dev/null; then
        check_item 1 "SECRET_KEY needs to be changed from default"
        FAILED=1
    else
        check_item 0 "SECRET_KEY appears to be configured"
    fi
else
    check_item 1 "Cannot verify SECRET_KEY - .env missing"
    FAILED=1
fi
echo ""

# Check 8: Port availability
echo "8. Checking port availability..."
PORTS=(80 443 8000 3000 9090)
for port in "${PORTS[@]}"; do
    if ! lsof -i:$port &> /dev/null; then
        check_item 0 "Port $port is available"
    else
        echo -e "${YELLOW}⚠${NC} Port $port is in use (may be intentional)"
    fi
done
echo ""

# Summary
echo "=================================================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review .env configuration"
    echo "  2. Run: docker-compose -f docker-compose.prod.yml up -d --build"
    echo "  3. Monitor: docker-compose -f docker-compose.prod.yml logs -f"
    echo "  4. Check health: curl http://localhost:8000/api/health"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please fix the issues above before deploying.${NC}"
    exit 1
fi
