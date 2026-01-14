# GIPIS Institucional - Flask App
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create instance directory for SQLite
RUN mkdir -p instance

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Expose port
EXPOSE 5000

# Run entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]

