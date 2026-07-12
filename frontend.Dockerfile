# Stage 1: Build
# Use Node.js LTS on Alpine for small builder image.
FROM node:20-alpine AS builder

WORKDIR /app

# Enable Corepack so npm respects project tooling if Bun/pnpm is later adopted.
RUN corepack enable

# Copy manifests before full source for layer caching.
COPY package.json package-lock.json* bun.lock* ./

# Install all deps (including dev) for build.
RUN npm install

# Copy full source and build TanStack Start / Vite app.
# Override Nitro preset from cloudflare-module to node-server so output runs in Docker.
# This is containerization-specific; project source is unchanged.
COPY . .
RUN NITRO_PRESET=node-server npm run build

# Stage 2: Production runtime
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=4173

# Copy build output from Nitro, preserving the .output directory structure.
# Docker COPY src/ dst/ copies contents; to keep the directory itself, use src/. dst/.
COPY --from=builder /app/.output ./.output

# Copy package.json to install only production deps in final image.
COPY --from=builder /app/package.json ./

# Install only production dependencies.
RUN npm install --omit=dev

# Create non-root user matching host UID 1000 (standard).
RUN addgroup -g 1001 appgroup && adduser -u 1001 -S appuser -G appgroup
USER appuser

EXPOSE 4173

# Health check using Node built-in http module.
HEALTHCHECK --interval=10s --timeout=3s --retries=3 --start-period=5s \
  CMD node -e "require('http').get('http://localhost:4173', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); })"

# Use project-defined preview script, binding to all interfaces.
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
