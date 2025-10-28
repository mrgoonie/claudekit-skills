#!/bin/bash
# Check GEMINI_API_KEY from multiple sources
# Priority: process env -> skill directory -> project root

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"

echo "Checking GEMINI_API_KEY availability..."
echo ""

# Priority 1: Check process environment
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ API key found in environment variable"
    echo "  Source: \$GEMINI_API_KEY"
    echo "  Value: ${GEMINI_API_KEY:0:10}...${GEMINI_API_KEY: -5}"
    exit 0
fi

# Priority 2: Check skill directory .env
SKILL_ENV="$SKILL_DIR/.env"
if [ -f "$SKILL_ENV" ]; then
    # Source the file and check
    if grep -q "GEMINI_API_KEY=" "$SKILL_ENV"; then
        KEY=$(grep "GEMINI_API_KEY=" "$SKILL_ENV" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
        if [ -n "$KEY" ]; then
            echo "✓ API key found in skill directory"
            echo "  Source: $SKILL_ENV"
            echo "  Value: ${KEY:0:10}...${KEY: -5}"
            exit 0
        fi
    fi
fi

# Priority 3: Check project root .env
PROJECT_ENV="$PROJECT_ROOT/.env"
if [ -f "$PROJECT_ENV" ]; then
    if grep -q "GEMINI_API_KEY=" "$PROJECT_ENV"; then
        KEY=$(grep "GEMINI_API_KEY=" "$PROJECT_ENV" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
        if [ -n "$KEY" ]; then
            echo "✓ API key found in project root"
            echo "  Source: $PROJECT_ENV"
            echo "  Value: ${KEY:0:10}...${KEY: -5}"
            exit 0
        fi
    fi
fi

# Not found
echo "✗ GEMINI_API_KEY not found in any location"
echo ""
echo "Checked locations (in priority order):"
echo "  1. Environment variable: \$GEMINI_API_KEY"
echo "  2. Skill directory: $SKILL_ENV"
echo "  3. Project root: $PROJECT_ENV"
echo ""
echo "To set API key, use one of these methods:"
echo ""
echo "Option 1 - Environment variable (recommended):"
echo "  export GEMINI_API_KEY='your-api-key-here'"
echo ""
echo "Option 2 - Skill directory:"
echo "  echo \"GEMINI_API_KEY=your-api-key-here\" > $SKILL_ENV"
echo ""
echo "Option 3 - Project root:"
echo "  echo \"GEMINI_API_KEY=your-api-key-here\" > $PROJECT_ENV"
echo ""
echo "Get your API key at: https://aistudio.google.com/apikey"
echo ""
exit 1
