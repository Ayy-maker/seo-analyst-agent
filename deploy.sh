#!/bin/bash
# SEO Analyst Agent - Deployment Script
# Deploys to: seo.theprofitplatform.com.au

set -euo pipefail

echo "========================================"
echo "🚀 Deploying SEO Analyst Agent"
echo "========================================"
echo ""

# Check if running as root for system operations
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  This script needs sudo privileges for system configuration"
    echo "    Please run with: sudo bash deploy.sh"
    exit 1
fi

PROJECT_DIR="/home/avi/projects/seoanalyst/seo-analyst-agent"
SERVICE_NAME="seo-analyst"

echo "📁 Project Directory: $PROJECT_DIR"
echo ""

# Step 1: Stop existing service if running
echo "1️⃣  Checking for existing service..."
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "   ⏸️  Stopping existing service..."
    systemctl stop $SERVICE_NAME
    echo "   ✅ Service stopped"
else
    echo "   ℹ️  No existing service running"
fi
echo ""

# Step 2: Install systemd service
echo "2️⃣  Installing systemd service..."
cp $PROJECT_DIR/seo-analyst.service /etc/systemd/system/
chmod 644 /etc/systemd/system/seo-analyst.service
systemctl daemon-reload
echo "   ✅ Service installed"
echo ""

# Step 3: Install Nginx configuration
echo "3️⃣  Installing Nginx configuration..."
cp $PROJECT_DIR/nginx-seo-analyst.conf /etc/nginx/sites-available/seo-analyst
ln -sf /etc/nginx/sites-available/seo-analyst /etc/nginx/sites-enabled/
echo "   ✅ Nginx config installed"
echo ""

# Step 4: Test Nginx configuration
echo "4️⃣  Testing Nginx configuration..."
if nginx -t; then
    echo "   ✅ Nginx config valid"
else
    echo "   ❌ Nginx config invalid - aborting"
    exit 1
fi
echo ""

# Step 5: Start and enable service
echo "5️⃣  Starting SEO Analyst service..."
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
sleep 2
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "   ✅ Service running"
else
    echo "   ❌ Service failed to start"
    echo "   View logs: sudo journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi
echo ""

# Step 6: Reload Nginx
echo "6️⃣  Reloading Nginx..."
systemctl reload nginx
echo "   ✅ Nginx reloaded"
echo ""

# Step 7: Setup SSL with Let's Encrypt
echo "7️⃣  Setting up SSL certificate..."
echo "   📋 Domain: seo.theprofitplatform.com.au"
echo ""
echo "   Running certbot..."

# Check if certificate already exists
if [ -d "/etc/letsencrypt/live/seo.theprofitplatform.com.au" ]; then
    echo "   ℹ️  Certificate already exists"
    echo "   Renewing certificate..."
    certbot --nginx -d seo.theprofitplatform.com.au --non-interactive --agree-tos --redirect
else
    echo "   Creating new certificate..."
    certbot --nginx -d seo.theprofitplatform.com.au --non-interactive --agree-tos --redirect
fi

if [ $? -eq 0 ]; then
    echo "   ✅ SSL certificate configured"
else
    echo "   ⚠️  SSL setup had issues - check manually"
    echo "   You can run: sudo certbot --nginx -d seo.theprofitplatform.com.au"
fi
echo ""

# Step 8: Final status check
echo "========================================"
echo "📊 Deployment Status"
echo "========================================"
echo ""

# Check service status
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ Service: Running"
else
    echo "❌ Service: Not running"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx: Running"
else
    echo "❌ Nginx: Not running"
fi

# Check if port 5001 is listening
if ss -tlnp | grep -q ":5001"; then
    echo "✅ Port 5001: Listening"
else
    echo "❌ Port 5001: Not listening"
fi

# Check DNS/connectivity
echo ""
echo "🌐 Testing connectivity..."
if curl -s -I http://seo.theprofitplatform.com.au > /dev/null 2>&1; then
    echo "✅ HTTP: Accessible"
else
    echo "⚠️  HTTP: Not accessible (may need DNS propagation)"
fi

if curl -s -I https://seo.theprofitplatform.com.au > /dev/null 2>&1; then
    echo "✅ HTTPS: Accessible"
else
    echo "⚠️  HTTPS: Not accessible (may need DNS propagation)"
fi

echo ""
echo "========================================"
echo "✅ Deployment Complete!"
echo "========================================"
echo ""
echo "🌐 Your SEO Analyst is now available at:"
echo "   https://seo.theprofitplatform.com.au"
echo ""
echo "📊 Useful commands:"
echo "   View logs:    sudo journalctl -u $SERVICE_NAME -f"
echo "   Restart:      sudo systemctl restart $SERVICE_NAME"
echo "   Stop:         sudo systemctl stop $SERVICE_NAME"
echo "   Status:       sudo systemctl status $SERVICE_NAME"
echo "   Nginx logs:   sudo tail -f /var/log/nginx/seo-analyst-*.log"
echo ""
