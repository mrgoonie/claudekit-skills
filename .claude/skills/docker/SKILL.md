---
name: docker
description: Guide for using Docker - a containerization platform for building, running, and deploying applications in isolated containers. Use when containerizing applications, creating Dockerfiles, working with Docker Compose, managing images/containers, configuring networking and storage, optimizing builds, deploying to production, or implementing CI/CD pipelines with Docker.
---

# Docker Skill

This skill provides comprehensive guidance for working with Docker, covering containerization concepts, practical workflows, and best practices across all major technology stacks.

## When to Use This Skill

Use this skill when:
- Containerizing applications for any language or framework
- Creating or optimizing Dockerfiles and Docker Compose configurations
- Setting up development environments with Docker
- Deploying containerized applications to production
- Implementing CI/CD pipelines with Docker
- Managing container networking, storage, and security
- Troubleshooting Docker-related issues
- Building multi-platform images
- Implementing microservices architectures

## Core Docker Concepts

### Containers
- **Lightweight, isolated processes** that bundle applications with all dependencies
- Provide filesystem isolation via union filesystems and namespace technology
- **Ephemeral by default** - changes are lost when container stops (unless persisted to volumes)
- **Single responsibility principle**: each container should do one thing well
- Multiple identical containers can run from same immutable image without conflicts

### Images
- **Blueprint/template for containers** - read-only filesystems + configuration
- Composed of **layered filesystem** (immutable, reusable layers)
- Built from Dockerfile instructions or committed from running containers
- Stored in registries (Docker Hub, ECR, ACR, GCR, private registries)
- **Image naming**: `REGISTRY/NAMESPACE/REPOSITORY:TAG` (e.g., `docker.io/library/nginx:latest`)

### Volumes & Storage
- **Volumes**: Docker-managed persistent storage that survives container deletion
- **Bind mounts**: Direct mapping of host filesystem paths into containers
- **tmpfs mounts**: In-memory storage for temporary data
- Enable data sharing between containers and persist beyond container lifecycle

### Networks
- **Default bridge network** connects containers on same host
- **Custom networks** allow explicit container communication with DNS resolution
- **Host network** removes network isolation for performance
- **Overlay networks** enable multi-host container communication (Swarm)
- **MACVLAN/IPvlan** for containers needing direct L2/L3 network access

## Dockerfile Best Practices

### Essential Instructions

```dockerfile
FROM <image>:<tag>                        # Base image (use specific versions, not 'latest')
WORKDIR /app                              # Working directory for subsequent commands
COPY package*.json ./                     # Copy dependency files first (for caching)
RUN npm install --production              # Execute build commands
COPY . .                                  # Copy application code
ENV NODE_ENV=production                   # Environment variables
EXPOSE 3000                               # Document exposed ports
USER node                                 # Run as non-root user (security)
CMD ["node", "server.js"]                 # Default command when container starts
```

### Multi-Stage Builds (Critical for Production)

Separate build environment from runtime environment to reduce image size and improve security:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Benefits**: Compiled assets without build tools in final image, smaller size, improved security

### Layer Caching Optimization

**Order matters!** Docker reuses layers if instruction unchanged:

1. **Dependencies first** (COPY package.json, RUN npm install)
2. **Application code last** (COPY . .)
3. This way, code changes don't invalidate dependency layers

### Security Hardening

```dockerfile
# Use specific versions
FROM node:20.11.0-alpine3.19

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set ownership
COPY --chown=nodejs:nodejs . .

# Switch to non-root
USER nodejs

# Read-only root filesystem (when possible)
# Add --read-only flag when running container
```

### .dockerignore File

Exclude unnecessary files from build context:

```
node_modules
.git
.env
.env.local
*.log
.DS_Store
README.md
docker-compose.yml
.dockerignore
Dockerfile
dist
coverage
.vscode
```

## Common Workflows

### Building Images

```bash
# Build with tag
docker build -t myapp:1.0 .

# Build targeting specific stage
docker build -t myapp:dev --target build .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp:1.0 .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:1.0 .

# View image layers and size
docker image history myapp:1.0

# List all images
docker image ls
```

### Running Containers

```bash
# Basic run
docker run myapp:1.0

# Run in background (detached)
docker run -d --name myapp myapp:1.0

# Port mapping (host:container)
docker run -p 8080:3000 myapp:1.0

# Environment variables
docker run -e NODE_ENV=production -e API_KEY=secret myapp:1.0

# Volume mount (named volume)
docker run -v mydata:/app/data myapp:1.0

# Bind mount (development)
docker run -v $(pwd)/src:/app/src myapp:1.0

# Custom network
docker run --network my-network myapp:1.0

# Resource limits
docker run --memory 512m --cpus 0.5 myapp:1.0

# Interactive terminal
docker run -it myapp:1.0 /bin/sh

# Override entrypoint/command
docker run --entrypoint /bin/sh myapp:1.0
docker run myapp:1.0 custom-command --arg
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View logs
docker logs myapp
docker logs -f myapp              # Follow logs
docker logs --tail 100 myapp      # Last 100 lines

# Execute command in running container
docker exec myapp ls /app
docker exec -it myapp /bin/sh     # Interactive shell

# Stop container (graceful)
docker stop myapp

# Kill container (immediate)
docker kill myapp

# Remove container
docker rm myapp
docker rm -f myapp                # Force remove running container

# View container details
docker inspect myapp

# Monitor resource usage
docker stats myapp

# View container processes
docker top myapp

# Copy files to/from container
docker cp myapp:/app/logs ./logs
docker cp ./config.json myapp:/app/config.json
```

### Image Management

```bash
# Tag image
docker tag myapp:1.0 registry.example.com/myapp:1.0

# Push to registry
docker login registry.example.com
docker push registry.example.com/myapp:1.0

# Pull from registry
docker pull nginx:alpine

# Remove image
docker image rm myapp:1.0

# Remove unused images
docker image prune

# Remove all unused resources (images, containers, volumes, networks)
docker system prune -a

# View disk usage
docker system df
```

### Volume Management

```bash
# Create named volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune
```

### Network Management

```bash
# Create network
docker network create my-network
docker network create --driver bridge my-bridge

# List networks
docker network ls

# Inspect network
docker network inspect my-network

# Connect container to network
docker network connect my-network myapp

# Disconnect container from network
docker network disconnect my-network myapp

# Remove network
docker network rm my-network
```

## Docker Compose

### When to Use Compose

- **Multi-container applications** (web + database + cache)
- **Consistent development environments** across team
- **Simplifying complex docker run commands**
- **Managing application dependencies** and startup order

### Basic Compose File Structure

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis
    volumes:
      - ./src:/app/src      # Development: live code reload
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    networks:
      - app-network
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### Compose Commands

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Build images before starting
docker compose up --build

# Scale specific service
docker compose up -d --scale web=3

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down --volumes

# View logs
docker compose logs
docker compose logs -f web        # Follow specific service

# Execute command in service
docker compose exec web sh
docker compose exec db psql -U user -d app

# List running services
docker compose ps

# Restart service
docker compose restart web

# Pull latest images
docker compose pull

# Validate compose file
docker compose config
```

### Development vs Production Compose

**compose.yml** (base configuration):
```yaml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
```

**compose.override.yml** (development overrides, loaded automatically):
```yaml
services:
  web:
    volumes:
      - ./src:/app/src      # Live code reload
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev
```

**compose.prod.yml** (production overrides):
```yaml
services:
  web:
    image: registry.example.com/myapp:1.0
    restart: always
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

**Usage**:
```bash
# Development (uses compose.yml + compose.override.yml automatically)
docker compose up

# Production (explicit override)
docker compose -f compose.yml -f compose.prod.yml up -d
```

## Language-Specific Dockerfiles

### Node.js

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Python

```dockerfile
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
```

### Go

```dockerfile
FROM golang:1.21-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM scratch
COPY --from=build /app/main /main
EXPOSE 8080
CMD ["/main"]
```

### Java (Spring Boot)

```dockerfile
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine AS production
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN addgroup -g 1001 -S spring && \
    adduser -S spring -u 1001
USER spring
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### React/Vue/Angular (Static SPA)

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Production Deployment

### Health Checks

**In Dockerfile**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

**In Compose**:
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      start-period: 40s
      retries: 3
```

### Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Restart Policies

```yaml
services:
  web:
    restart: unless-stopped    # Restart unless manually stopped
    # Other options: "no", "always", "on-failure"
```

### Logging Configuration

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Environment Variables & Secrets

**Using .env file**:
```bash
# .env
DATABASE_URL=postgresql://user:pass@db:5432/app
API_KEY=secret
```

```yaml
services:
  web:
    env_file:
      - .env
```

**Using Docker secrets** (Swarm):
```yaml
services:
  web:
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

### Production Checklist

- ✅ Use specific image versions (not `latest`)
- ✅ Run as non-root user
- ✅ Multi-stage builds to minimize image size
- ✅ Health checks implemented
- ✅ Resource limits configured
- ✅ Restart policy set
- ✅ Logging configured
- ✅ Secrets managed securely (not in environment variables)
- ✅ Vulnerability scanning (Docker Scout)
- ✅ Read-only root filesystem when possible
- ✅ Network segmentation
- ✅ Regular image updates

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: user/app:latest,user/app:${{ github.sha }}
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max

      - name: Run vulnerability scan
        uses: docker/scout-action@v1
        with:
          command: cves
          image: user/app:${{ github.sha }}
```

## Security Best Practices

### Scan for Vulnerabilities

```bash
# Using Docker Scout
docker scout cves myapp:1.0
docker scout recommendations myapp:1.0

# Quick view
docker scout quickview myapp:1.0
```

### Run Containers Securely

```bash
# Read-only root filesystem
docker run --read-only -v /tmp --tmpfs /run myapp:1.0

# Drop all capabilities, add only needed ones
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp:1.0

# No new privileges
docker run --security-opt=no-new-privileges myapp:1.0

# Use security profiles
docker run --security-opt apparmor=docker-default myapp:1.0

# Limit resources
docker run --memory=512m --cpus=0.5 --pids-limit=100 myapp:1.0
```

### Image Security Checklist

- ✅ Start with minimal base images (Alpine, Distroless)
- ✅ Use specific versions, not `latest`
- ✅ Scan for vulnerabilities regularly
- ✅ Run as non-root user
- ✅ Don't include secrets in images (use runtime secrets)
- ✅ Minimize attack surface (only install needed packages)
- ✅ Use multi-stage builds (no build tools in final image)
- ✅ Sign and verify images
- ✅ Keep images updated

## Networking Patterns

### Bridge Network (Default)

```bash
# Create custom bridge network
docker network create my-bridge

# Run containers on custom bridge
docker run -d --name web --network my-bridge nginx
docker run -d --name db --network my-bridge postgres

# Containers can communicate via container name
# web can connect to: http://db:5432
```

### Container Communication

```yaml
services:
  web:
    depends_on:
      - db
    environment:
      # Use service name as hostname
      - DATABASE_URL=postgresql://user:pass@db:5432/app

  db:
    image: postgres:15-alpine
```

### Port Publishing

```bash
# Publish single port
docker run -p 8080:80 nginx

# Publish range of ports
docker run -p 8080-8090:8080-8090 myapp

# Publish to specific interface
docker run -p 127.0.0.1:8080:80 nginx

# Publish all exposed ports to random ports
docker run -P nginx
```

## Storage Patterns

### Named Volumes (Recommended for Data)

```bash
# Create and use named volume
docker volume create app-data
docker run -v app-data:/app/data myapp

# Automatic creation
docker run -v app-data:/app/data myapp  # Creates if doesn't exist
```

### Bind Mounts (Development)

```bash
# Live code reload during development
docker run -v $(pwd)/src:/app/src myapp

# Read-only bind mount
docker run -v $(pwd)/config:/app/config:ro myapp
```

### tmpfs Mounts (Temporary In-Memory)

```bash
# Store temporary data in memory
docker run --tmpfs /tmp myapp
```

### Volume Backup & Restore

```bash
# Backup volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/backup.tar.gz -C /data
```

## Troubleshooting

### Debug Running Container

```bash
# View logs
docker logs -f myapp
docker logs --tail 100 myapp

# Interactive shell
docker exec -it myapp /bin/sh

# Inspect container
docker inspect myapp

# View processes
docker top myapp

# Monitor resource usage
docker stats myapp

# View changes to filesystem
docker diff myapp
```

### Debug Build Issues

```bash
# Build with verbose output
docker build --progress=plain -t myapp .

# Build specific stage for testing
docker build --target build -t myapp:build .

# Run failed build stage
docker run -it myapp:build /bin/sh

# Check build context
docker build --no-cache -t myapp .
```

### Common Issues

**Container exits immediately**:
```bash
# Check logs
docker logs myapp

# Run with interactive shell
docker run -it myapp /bin/sh

# Override entrypoint
docker run -it --entrypoint /bin/sh myapp
```

**Cannot connect to container**:
```bash
# Check port mapping
docker ps
docker port myapp

# Check network
docker network inspect bridge
docker inspect myapp | grep IPAddress

# Check if service is listening
docker exec myapp netstat -tulpn
```

**Out of disk space**:
```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a
docker volume prune
docker image prune -a
```

**Build cache issues**:
```bash
# Force rebuild without cache
docker build --no-cache -t myapp .

# Clear build cache
docker builder prune
```

## Advanced Topics

### Multi-Platform Builds

```bash
# Setup buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myapp:1.0 --push .
```

### Build Optimization

```bash
# Use BuildKit (enabled by default in recent versions)
DOCKER_BUILDKIT=1 docker build -t myapp .

# Use build cache from registry
docker build --cache-from myapp:latest -t myapp:1.0 .

# Export cache to registry
docker build --cache-to type=registry,ref=myapp:buildcache \
  --cache-from type=registry,ref=myapp:buildcache \
  -t myapp:1.0 .
```

### Docker Contexts

```bash
# List contexts
docker context ls

# Create remote context
docker context create remote --docker "host=ssh://user@remote"

# Use context
docker context use remote
docker ps  # Now runs on remote host

# Switch back to default
docker context use default
```

## Quick Reference

### Most Common Commands

| Task | Command |
|------|---------|
| Build image | `docker build -t myapp:1.0 .` |
| Run container | `docker run -d -p 8080:3000 myapp:1.0` |
| View logs | `docker logs -f myapp` |
| Shell into container | `docker exec -it myapp /bin/sh` |
| Stop container | `docker stop myapp` |
| Remove container | `docker rm myapp` |
| Start Compose | `docker compose up -d` |
| Stop Compose | `docker compose down` |
| View Compose logs | `docker compose logs -f` |
| Clean up all | `docker system prune -a` |

### Recommended Base Images

| Language/Framework | Recommended Base |
|-------------------|------------------|
| Node.js | `node:20-alpine` |
| Python | `python:3.11-slim` |
| Java | `eclipse-temurin:21-jre-alpine` |
| Go | `scratch` (for compiled binary) |
| .NET | `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` |
| PHP | `php:8.2-fpm-alpine` |
| Ruby | `ruby:3.2-alpine` |
| Static sites | `nginx:alpine` |

## Additional Resources

- **Official Documentation**: https://docs.docker.com
- **Docker Hub**: https://hub.docker.com (public image registry)
- **Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Security**: https://docs.docker.com/engine/security/
- **Dockerfile Reference**: https://docs.docker.com/engine/reference/builder/
- **Compose Specification**: https://docs.docker.com/compose/compose-file/

## Summary

Docker containerization provides:
- **Consistency** across development, testing, and production
- **Isolation** for applications and dependencies
- **Portability** across different environments
- **Efficiency** through layered architecture and caching
- **Scalability** for microservices and distributed systems

Follow multi-stage builds, run as non-root, use specific versions, implement health checks, scan for vulnerabilities, and configure resource limits for production-ready containerized applications.
