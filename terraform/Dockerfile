# Dockerfile for tflocal
FROM hashicorp/terraform:latest

# Install Python and pip
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir terraform-local && \
    pip3 install --no-cache-dir awscli-local

ENTRYPOINT ["sh"]
