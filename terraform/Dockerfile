# Dockerfile for tflocal
FROM python:3.9-alpine as python_base

# Install dependencies
RUN apk add --no-cache bash

# Create a virtual environment
RUN python -m venv /opt/venv

# Install the required Python packages within the virtual environment
RUN /opt/venv/bin/pip install --no-cache-dir terraform-local awscli-local

# Use hashicorp/terraform as the base image for the final stage
FROM hashicorp/terraform:latest

# Copy the virtual environment from the previous stage
COPY --from=python_base /opt/venv /opt/venv

# Set the virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["sh"]
