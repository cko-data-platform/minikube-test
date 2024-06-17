# Dockerfile for tflocal
FROM python:3.9-alpine

# Install bash, curl, and unzip
RUN apk add --no-cache bash curl unzip groff less

# Define Terraform version
ENV TERRAFORM_VERSION=1.5.0

# Download and install Terraform
RUN curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform.zip && \
    unzip terraform.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform.zip

# Install the required Python packages globally
RUN pip install --no-cache-dir terraform-local awscli-local awscli

ENTRYPOINT ["sh"]
