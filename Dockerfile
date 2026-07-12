FROM node:22-alpine AS build

WORKDIR /app

COPY package.json bun.lock bunfig.toml ./
RUN npm install --no-audit --no-fund

COPY . .

ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
