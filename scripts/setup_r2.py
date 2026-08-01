import os
import subprocess
import sys

def setup_dvc_r2():
    print("==========================================")
    print("Setting up Cloudflare R2 Remote for DVC")
    print("==========================================")

    endpoint = os.getenv("R2_ENDPOINT_URL")
    bucket = os.getenv("R2_BUCKET_NAME", "cardio-ai-datasets")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not endpoint or not access_key or not secret_key:
        print("\n❌ Missing R2 Environment Variables!")
        print("Please copy .env.example to .env and set your Cloudflare R2 credentials.")
        print("\nRequired variables in .env:")
        print("  R2_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com")
        print("  R2_BUCKET_NAME=cardio-ai-datasets")
        print("  AWS_ACCESS_KEY_ID=your_access_key_id")
        print("  AWS_SECRET_ACCESS_KEY=your_secret_access_key")
        sys.exit(1)

    print(f"\nConfiguring DVC remote 'r2' pointing to s3://{bucket}...")
    subprocess.run(["dvc", "remote", "add", "-f", "r2", f"s3://{bucket}"], check=True)
    subprocess.run(["dvc", "remote", "modify", "r2", "endpointurl", endpoint], check=True)
    subprocess.run(["dvc", "config", "core.remote", "r2"], check=True)
    
    print("\n✅ DVC Cloudflare R2 Remote Configured Successfully!")
    print("Commands available:")
    print("  dvc push   -> Push datasets/models to Cloudflare R2")
    print("  dvc pull   -> Pull datasets/models from Cloudflare R2")

if __name__ == "__main__":
    setup_dvc_r2()
