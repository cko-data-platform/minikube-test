# Dockerfile for tflocal
FROM hashicorp/terraform:latest

# Install Python, pip, and virtualenv
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir virtualenv

# Create a virtual environment and activate it
RUN virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the required Python packages within the virtual environment
RUN pip install --no-cache-dir terraform-local awscli-local

ENTRYPOINT ["sh"]
