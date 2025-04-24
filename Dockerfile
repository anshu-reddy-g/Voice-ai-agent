# 1. Pin to a specific Python version
FROM python:3.12-slim

# 2. Set app directory
WORKDIR /app

# 3. Copy only requirements first (caching layer)
COPY requirements.txt ./

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your app code and env file (optional—you can also mount .env at runtime)
COPY . .

# 6. Expose the port FastAPI listens on
EXPOSE 8000

# 7. Tell Python where to find your GCP key
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/voice-agent-key.json

# 8. Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
