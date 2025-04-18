FROM node:18

WORKDIR /app

# Copy package definition and install dependencies
COPY . /app
COPY zscaler.crt /usr/local/share/ca-certificates/zscaler.crt

RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates && \
    npm install

# Set default port (can be overridden)
ENV PORT=8080
EXPOSE 8080

# Start the server
CMD ["node", "server.js"]