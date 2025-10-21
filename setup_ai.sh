#!/bin/bash

# AI Insights Quick Setup Script
# Guides user through adding Anthropic API key

set -e

PROJECT_DIR="/home/avi/projects/seoanalyst/seo-analyst-agent"
ENV_FILE="$PROJECT_DIR/.env"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🤖 SEO Analyst AI Insights - Quick Setup"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "⚠️  Don't run this script as root. Run as user 'avi'."
   exit 1
fi

# Check current API key status
echo "📋 Checking current configuration..."
echo ""

if [ -f "$ENV_FILE" ]; then
    current_key=$(grep "ANTHROPIC_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)

    if [ "$current_key" == "your_api_key_here" ] || [ -z "$current_key" ]; then
        echo "⚠️  Status: No API key configured (placeholder detected)"
    else
        echo "✅ Status: API key found"
        echo "   Current: ${current_key:0:15}...${current_key: -4} (${#current_key} chars)"
        echo ""
        read -p "   Do you want to replace the existing key? (y/N): " replace
        if [[ ! $replace =~ ^[Yy]$ ]]; then
            echo ""
            echo "   Keeping existing key. Exiting."
            echo ""
            exit 0
        fi
    fi
else
    echo "❌ Error: .env file not found at $ENV_FILE"
    exit 1
fi

echo ""
echo "────────────────────────────────────────────────────────────────"
echo "🔑 Adding Anthropic API Key"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "1. Open: https://console.anthropic.com/"
echo "2. Sign in or create an account"
echo "3. Go to: API Keys section"
echo "4. Click: Create Key"
echo "5. Copy the key (starts with 'sk-ant-api03-...')"
echo ""

# Prompt for API key
read -p "Paste your Anthropic API key here: " api_key

# Validate basic format
if [[ ! $api_key =~ ^sk-ant-api ]]; then
    echo ""
    echo "❌ Error: Invalid API key format"
    echo "   Key should start with 'sk-ant-api03-'"
    echo "   Please try again."
    echo ""
    exit 1
fi

echo ""
echo "📝 Updating .env file..."

# Backup existing .env
cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%Y%m%d_%H%M%S)"

# Update API key in .env
sed -i "s/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$api_key/" "$ENV_FILE"

# Verify permissions
chmod 600 "$ENV_FILE"

echo "✅ API key added successfully!"
echo ""

echo "────────────────────────────────────────────────────────────────"
echo "🔄 Restarting SEO Analyst Service"
echo "────────────────────────────────────────────────────────────────"
echo ""

# Restart service
sudo systemctl restart seo-analyst

# Wait for service to start
sleep 3

# Check service status
if sudo systemctl is-active --quiet seo-analyst; then
    echo "✅ Service restarted successfully!"
else
    echo "❌ Error: Service failed to start"
    echo "   Check logs: sudo journalctl -u seo-analyst -n 50"
    exit 1
fi

echo ""
echo "────────────────────────────────────────────────────────────────"
echo "🧪 Testing AI Configuration"
echo "────────────────────────────────────────────────────────────────"
echo ""

# Run test
cd "$PROJECT_DIR"
source venv/bin/activate
python test_ai_setup.py

echo ""
echo "────────────────────────────────────────────────────────────────"
echo "✅ Setup Complete!"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "Next steps:"
echo "  1. Visit: https://seo.theprofitplatform.com.au"
echo "  2. Upload a SEMrush file for any client"
echo "  3. View the AI-generated insights in the report"
echo ""
echo "Expected improvements:"
echo "  ✅ Industry-aware executive summaries"
echo "  ✅ Specific, actionable recommendations"
echo "  ✅ Prioritized action items (Quick Wins, High Impact)"
echo "  ✅ ROI estimates and impact projections"
echo "  ✅ Competitive benchmarking"
echo ""
echo "Documentation: $PROJECT_DIR/AI_INSIGHTS_SETUP.md"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
