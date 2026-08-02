# CardioSense ML — Deployment Reference

> **DADMP v1.0 — Combined Deployment Reference**  
> Quick-access guide for both deployment models.

---

## Local Development (No Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (port 5000 locally)
PORT=5000 FLASK_DEBUG=true python app.py

# 3. Open browser
# http://localhost:5000
```

---

## Model 1 — Hugging Face Spaces (Recommended for Portfolio)

See the full guide: **[infra/cloud/DEPLOYMENT_GUIDE.md](../infra/cloud/DEPLOYMENT_GUIDE.md)**

Quick summary:
```bash
# Add HF remote (one-time)
git remote add hf https://huggingface.co/spaces/[your-hf-username]/cardiosense-ml

# Deploy
git push hf main
```

**Live URL:** `https://[username]-cardiosense-ml.hf.space`

---

## Model 2 — Self-Hosted Docker Compose

```bash
# 1. Copy and fill environment variables
cp infra/docker/.env.example infra/docker/.env

# 2. Start the full stack (app + MinIO + Nginx)
docker-compose -f infra/docker/docker-compose.yml up -d

# 3. Check status
docker-compose -f infra/docker/docker-compose.yml ps

# 4. View logs
docker-compose -f infra/docker/docker-compose.yml logs -f app

# 5. Stop
docker-compose -f infra/docker/docker-compose.yml down
```

**Access:**
- App: `http://localhost:80`
- MinIO Console: `http://localhost:9001`

### Production VPS Deployment
```bash
# On your VPS (after cloning the repo)
docker-compose -f infra/docker/docker-compose.yml \
               -f infra/docker/docker-compose.prod.yml up -d
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `PORT` | No | `7860` | Port the Flask app listens on |
| `FLASK_DEBUG` | No | `false` | Enable Flask debug mode |
| `SECRET_KEY` | **Yes (prod)** | — | Flask session secret |
| `MINIO_ROOT_USER` | No | `minioadmin` | MinIO admin username |
| `MINIO_ROOT_PASSWORD` | No | `minioadmin` | MinIO admin password |
| `MINIO_BUCKET` | No | `cardiosense-uploads` | MinIO default bucket |
| `R2_ENDPOINT_URL` | No | — | Cloudflare R2 endpoint |
| `SENTRY_DSN` | No | — | Sentry error tracking DSN |

---

## CI/CD (GitHub Actions → Hugging Face)

Add this to `.github/workflows/deploy-hf.yml` to auto-deploy on every push to `main`:

```yaml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          lfs: true

      - name: Push to Hugging Face Spaces
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git remote add hf https://[username]:$HF_TOKEN@huggingface.co/spaces/[username]/cardiosense-ml
          git push hf main --force
```

> Add `HF_TOKEN` (your HF API token) as a GitHub repository secret.
