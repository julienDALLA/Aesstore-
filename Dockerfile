# Dockerfile for Aesstore Fullstack Application
# This is a multi-stage build for development

# Stage 1: Build backend dependencies
FROM python:3.11-slim as backend-deps

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Build frontend dependencies
FROM node:18-alpine as frontend-deps

WORKDIR /app

# Install frontend dependencies
COPY frontend/package.json frontend/tsconfig.json frontend/next.config.js ./
RUN npm install

# Stage 3: Final production image
FROM python:3.11-slim as production

WORKDIR /app

# Install system dependencies for production
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend-deps stage
COPY --from=backend-deps /root/.local /root/.local
COPY --from=backend-deps /app/requirements.txt .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy backend source code
COPY backend/ ./backend/

# Create necessary directories
RUN mkdir -p uploads logs static

# Copy frontend build from frontend-deps stage
COPY --from=frontend-deps /app/node_modules ./frontend/node_modules
COPY frontend/ ./frontend/

# Build frontend
WORKDIR /app/frontend
RUN npm run build
WORKDIR /app

# Install serve for frontend
RUN npm install -g serve

# Copy built frontend to static
RUN cp -r frontend/out static/frontend

# Set environment variables
ENV PYTHONPATH=/app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health').raise_for_status()" || exit 1

# Start the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
