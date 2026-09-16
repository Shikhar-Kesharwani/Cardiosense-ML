# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile — CardioSense ML (Hugging Face Spaces compatible)
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.10-slim

# Hugging Face Spaces requires the app to run as a non-root user (UID 1000)
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    # Default port for Hugging Face Spaces. Override with PORT env var locally.
    PORT=7860

WORKDIR $HOME/app

# Install dependencies first (cached layer — only rebuilds when requirements change)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY --chown=user . .

# Hugging Face Spaces REQUIRES port 7860
EXPOSE 7860

# Start the Flask application via gunicorn for production stability
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120", "app:app"]
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
