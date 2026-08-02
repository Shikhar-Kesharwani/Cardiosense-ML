# Hugging Face Spaces Deployment — Step by Step

> **Model 1 — Cloud-Native Deployment for CardioSense ML**  
> Platform: Hugging Face Spaces (Docker SDK)  
> Free Tier: 2 vCPU, 16GB RAM — fully capable of running catboost, xgboost, scikit-learn  
> Live URL format: `https://[username]-[space-name].hf.space`

---

## Step 1: Create a Hugging Face Account & Space

1. Go to **[huggingface.co](https://huggingface.co)** → Sign In / Sign Up (free).
2. Click your avatar (top right) → **New Space**.
3. Fill in the form:
   - **Space Name:** `cardiosense-ml` (or any name you like)
   - **License:** MIT
   - **Select SDK:** → Click **Docker** → Select **Blank**
   - **Hardware:** Free (2 vCPU, 16GB RAM) ← **This is all you need**
   - **Visibility:** Public (required for free hardware)
4. Click **Create Space**.

---

## Step 2: Add Environment Variables (Secrets)

Before pushing code, add your secrets in the Space settings:

1. In your Space → Click **Settings** tab → Scroll to **Variables and Secrets**.
2. Add the following:

| Key | Value |
|---|---|
| `PORT` | `7860` |
| `FLASK_DEBUG` | `false` |

> Do NOT add any API keys in plaintext. Use the **Secret** type for any sensitive values.

---

## Step 3: Push Your Code to Hugging Face

### Option A — Git Push (Recommended)

```bash
# One-time: add Hugging Face as a remote
git remote add hf https://huggingface.co/spaces/[your-hf-username]/cardiosense-ml

# Push your code to Hugging Face
git push hf main
```

> Replace `[your-hf-username]` with your actual Hugging Face username.

### Option B — Manual Upload

1. In your Space → Click the **Files** tab.
2. Upload all project files. Ensure these are at the root:
   - `Dockerfile`
   - `requirements.txt`
   - `app.py`
   - `src/` directory
   - `models/` directory (with your `.pkl` model files)
   - `templates/` and `static/` directories

---

## Step 4: Wait for Build (~3–7 minutes)

1. Click the **App** tab in your Space to watch the build logs.
2. You will see:
   ```
   Building Docker image...
   Installing requirements...
   Starting gunicorn...
   Running on port 7860
   ```
3. Once complete, your app is live at:
   ```
   https://[your-hf-username]-cardiosense-ml.hf.space
   ```

This is your **permanent portfolio/interview link**. It runs 24/7 as long as the Space is Public.

---

## Step 5: Set Up Model Files (Important!)

Your `.pkl` model files are in `models/` and gitignored locally (for security). For Hugging Face, you have two options:

### Option A — Upload models directly (Simplest)
Upload the `models/` folder manually via the **Files** tab in your HF Space.

### Option B — Use Hugging Face Hub (Recommended for large models)
```python
# Install: pip install huggingface_hub
from huggingface_hub import hf_hub_download
# Download model at runtime from a private/public HF model repo
```

---

## Step 6: Custom Domain (Optional)

Hugging Face Spaces supports custom domains on the Pro plan. For the free tier, your URL will always be:
`https://[username]-[space-name].hf.space`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Build fails with `ModuleNotFoundError` | Ensure `requirements.txt` includes all dependencies |
| App shows blank screen | Check that `PORT=7860` env var is set in Space Settings |
| Model not found error | Upload `models/` folder manually via Files tab |
| Build timeout | Reduce requirements (remove unused packages from requirements.txt) |

---

## Your Live URL After Deployment

```
https://[your-hf-username]-cardiosense-ml.hf.space
```

Share this link in your portfolio, LinkedIn, and interviews!
