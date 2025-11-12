# 1. ✅ Add base image
FROM python:3.12.0-slim-bookworm

# 2. Environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

# 3. ✅ Change working directory
WORKDIR $APP

# 4. ✅ Install and update Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. ✅ Add requirements.txt
COPY requirements.txt $APP/

# 6. Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# 7. Copy application files
COPY . $APP/

# 8. ✅ Expose port
EXPOSE 8000

# 9. Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# 10. ✅ Run command to start application
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
