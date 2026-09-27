# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY --chown=1000:1000 . .

# Run the web application without root privileges
RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --create-home app \
    && mkdir -p /data /uploads \
    && chown -R app:app /app /data /uploads
VOLUME ["/data", "/uploads"]

# Set environment variable for database path
ENV SQLITE_PATH=/data/db.sqlite3

# Make the start.sh script executable
RUN chmod +x /app/start.sh

USER app

# Expose the port used by the application
EXPOSE 8000

# Start the application using the start.sh script
CMD ["/app/start.sh"]
