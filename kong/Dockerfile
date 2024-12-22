# Use the official Kong image as the base
FROM kong:latest

# Switch to root user to install tools
USER root

# Install required tools: curl, jq, and any other dependencies
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    jq \
    coreutils \
    && apt-get clean

# Copy scripts into the container
COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/configure.sh /configure.sh

# Make the scripts executable
RUN chmod +x /entrypoint.sh /configure.sh

# Switch back to the default Kong user
USER kong

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["kong", "start"]
