# GitHub Integration Setup Guide

## Current Status

✅ Code committed locally with production deployment infrastructure
❌ Push to GitHub requires write access to `Ayy-maker/seo-analyst-agent`

**Current Permissions**: `Theprofitplatform` account has READ-only access

---

## Option 1: Add Collaborator (Recommended)

**Steps for repository owner (Ayy-maker):**

1. Go to https://github.com/Ayy-maker/seo-analyst-agent/settings/access
2. Click "Add people"
3. Add `Theprofitplatform` as a collaborator with **Write** access
4. Accept the invitation

**Then push from VPS:**
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
git push origin main
```

---

## Option 2: Personal Access Token

**Create a token for Ayy-maker account:**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy the token

**Update git credentials on VPS:**
```bash
# Update git credentials file
echo "https://Ayy-maker:YOUR_TOKEN_HERE@github.com" > ~/.git-credentials

# Or use gh CLI
gh auth login
```

**Then push:**
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
git remote set-url origin https://github.com/Ayy-maker/seo-analyst-agent.git
git push origin main
```

---

## Option 3: SSH Key Authentication

**Add SSH key to Ayy-maker account:**

1. Copy public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

2. Go to https://github.com/settings/keys
3. Click "New SSH key"
4. Paste the public key
5. Save

**Then push:**
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
git remote set-url origin git@github.com:Ayy-maker/seo-analyst-agent.git
git push origin main
```

---

## Required GitHub Actions Secrets

Once you have push access, configure these secrets at:
https://github.com/Ayy-maker/seo-analyst-agent/settings/secrets/actions

### 1. SSH_PRIVATE_KEY

**Purpose**: Allows GitHub Actions to deploy to VPS

**Get the private key from VPS:**
```bash
cat ~/.ssh/id_ed25519
```

**Add to GitHub:**
- Name: `SSH_PRIVATE_KEY`
- Value: Entire contents of the private key file (including `-----BEGIN` and `-----END` lines)

### 2. ANTHROPIC_API_KEY (Optional)

**Purpose**: Enables AI-powered insights in SEO reports

**Note**: This is optional. The SEO Analyst works without it, but AI insights enhance reports.

If you have an Anthropic API key:
- Name: `ANTHROPIC_API_KEY`
- Value: Your Anthropic API key (starts with `sk-ant-api03-`)

---

## Automated Deployment Workflow

Once secrets are configured, the CI/CD pipeline will:

1. **On Push to Main**:
   - Build Docker image
   - Push to GitHub Container Registry (GHCR)
   - SSH into VPS
   - Pull latest image
   - Deploy with health checks
   - Rollback automatically if deployment fails

2. **Deployment Location**: `/srv/apps/seo-analyst/`
3. **Production URL**: https://seo.theprofitplatform.com.au

---

## Manual Deployment (Without CI/CD)

If you prefer not to use GitHub Actions, deploy manually:

```bash
# SSH into VPS
ssh avi@31.97.222.218

# Navigate to deployment directory
cd /srv/apps/seo-analyst

# Pull latest changes
git pull

# Rebuild Docker image
docker compose build

# Deploy with health check
./deploy.sh latest
```

---

## Verify Deployment

After pushing to GitHub and configuring secrets:

1. **Check GitHub Actions**: https://github.com/Ayy-maker/seo-analyst-agent/actions
2. **Monitor deployment logs** in the Actions tab
3. **Verify production**: https://seo.theprofitplatform.com.au
4. **Check container status**:
```bash
ssh avi@31.97.222.218 'docker ps | grep seo-analyst'
```

---

## Current Commit

The following changes are committed locally and ready to push:

```
feat: Add production deployment infrastructure

- Multi-stage Dockerfile for optimized builds (816MB)
- Non-root container user (UID 1000) for security
- Fixed database directory conflict (/app/data for SQLite)
- GitHub Actions CI/CD workflow with rollback support
- Resource limits: 512MB RAM, 1 CPU
- Health checks and automated deployment to VPS
```

**Files modified:**
- `Dockerfile` - Production build configuration
- `.github/workflows/deploy.yml` - CI/CD pipeline

---

## Quick Start

1. **Choose authentication method** (Option 1, 2, or 3 above)
2. **Push to GitHub**: `git push origin main`
3. **Configure secrets** if using CI/CD
4. **Verify deployment** at https://seo.theprofitplatform.com.au

---

## Troubleshooting

### "Permission denied" on push
- Verify you have write access to the repository
- Check your authentication method (token/SSH key)
- Ensure credentials are correct

### GitHub Actions failing
- Verify `SSH_PRIVATE_KEY` secret is set correctly
- Check that the VPS SSH fingerprint is accepted
- Review deployment logs in Actions tab

### Container not starting
- Check logs: `docker compose logs -f`
- Verify volume permissions: `ls -la /srv/data/seo-analyst/`
- Check resource usage: `docker stats seo-analyst`

---

## Support

- **VPS Access**: `ssh avi@31.97.222.218`
- **Deployment Logs**: `/srv/apps/seo-analyst/`
- **Container Logs**: `docker compose logs -f`
- **Production URL**: https://seo.theprofitplatform.com.au
