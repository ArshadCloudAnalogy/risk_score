FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN yum update -y && yum install -y git openssh;

# Install Python dependencies
WORKDIR /var/task
COPY requirements.txt /var/task
RUN pip install --no-cache-dir --requirement /var/task/requirements.txt

# Copy application code
COPY . /var/task
# Make entrypoint script executable
RUN chmod +x docker-utils/entrypoint.sh

# Expose port for local testing (only needed for local environments)
EXPOSE 8000

# Set CMD
CMD ["./docker-utils/entrypoint.sh"]