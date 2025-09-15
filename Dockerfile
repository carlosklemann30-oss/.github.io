# Lightweight image for running the image optimization script
FROM python:3.12-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the script by default; mount the repo as a volume when running
COPY optimize_images.py ./

# Default to running the optimizer. Provide paths as args.
ENTRYPOINT ["python", "optimize_images.py"]
# By default, process the local images folder (override as needed)
CMD ["images"]

