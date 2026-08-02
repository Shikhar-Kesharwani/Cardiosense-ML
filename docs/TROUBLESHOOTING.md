# CardioSense ML — Troubleshooting Guide

> Common issues and fixes for both deployment models.

---

## Model 1 — Hugging Face Spaces

### ❌ Build Fails: `ModuleNotFoundError`
**Cause:** A package is missing from `requirements.txt`.  
**Fix:** Add the missing package to `requirements.txt` and re-push.

### ❌ App Shows Blank Page / `Connection refused`
**Cause:** The app is not listening on port 7860.  
**Fix:**
1. Ensure `PORT=7860` is set in your Space → Settings → Variables.
2. Verify `Dockerfile` has `EXPOSE 7860`.
3. Verify `CMD` uses port 7860: `gunicorn --bind 0.0.0.0:7860 app:app`.

### ❌ `Model file not found` Error
**Cause:** `.pkl` model files are gitignored and weren't pushed to HF Space.  
**Fix:** Manually upload the `models/` directory via the HF Space **Files** tab.

### ❌ Build Timeout (> 10 minutes)
**Cause:** Large packages (catboost) take time to install.  
**Fix:** This is expected on first build. Subsequent builds use Docker layer cache and are faster (~2 min).

### ❌ `git push hf main` Rejected
**Cause:** Large files (notebooks, datasets) exceed HF's 5GB limit.  
**Fix:** Ensure `.gitignore` excludes `Notebook_Experiments/`, `*.csv`, and `models/`.

---

## Model 2 — Docker Compose

### ❌ `docker-compose up` Fails: `Port 80 already in use`
**Cause:** Another service (Apache, another Nginx) is using port 80.  
**Fix:** In `infra/docker/.env`, change the Nginx port:
```bash
# Edit docker-compose.yml nginx ports section:
ports:
  - "8080:80"   # Use 8080 instead of 80
```

### ❌ App Container Exits Immediately
**Cause:** Missing environment variables or model files.  
**Fix:**
```bash
docker-compose -f infra/docker/docker-compose.yml logs app
```
Check the output for the specific error.

### ❌ MinIO Console Not Accessible (`localhost:9001`)
**Cause:** Container not started or port conflict.  
**Fix:**
```bash
docker-compose -f infra/docker/docker-compose.yml ps     # Check all containers
docker-compose -f infra/docker/docker-compose.yml restart minio
```

### ❌ Changes Not Reflected After `git push`
**Cause:** Docker is using a cached image layer.  
**Fix:**
```bash
docker-compose -f infra/docker/docker-compose.yml build --no-cache app
docker-compose -f infra/docker/docker-compose.yml up -d
```

### ❌ `Nginx 502 Bad Gateway`
**Cause:** App container is not running or is still starting up.  
**Fix:** Wait 30 seconds for the app to fully start (ML model loading takes time), then refresh.

---

## Local Development

### ❌ `ModuleNotFoundError: No module named 'src'`
**Cause:** Running `python app.py` from the wrong directory.  
**Fix:** Always run from the project root:
```bash
cd /path/to/heart_disease_prediction
python app.py
```

### ❌ Model prediction returns wrong results
**Cause:** Wrong model file loaded, or preprocessor mismatch.  
**Fix:** Verify model files in `models/` match the expected filenames in `src/Heart/pipeline/Prediction_pipeline.py`.

---

## Security Issues

### ❌ Git accidentally committed `.env` file
**Fix:**
```bash
# Remove from git tracking (keeps file locally)
git rm --cached .env
git commit -m "security: remove accidentally committed .env file"
git push

# Immediately rotate ALL secrets in that .env file
# Generate new SECRET_KEY, new API keys, etc.
```

### ❌ Large model files accidentally committed to git
**Fix:**
```bash
# Remove from git history (safe — file stays on disk)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch models/your_model.pkl" \
  --prune-empty --tag-name-filter cat -- --all
git push --force
```
