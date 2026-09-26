FROM node:20-alpine AS frontend
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY index.html postcss.config.js tailwind.config.js vite.config.js ./
COPY src ./src
COPY public ./public
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY backend/server.py ./backend/server.py
COPY --from=frontend /app/dist ./dist
ENV NAI_HOST=0.0.0.0 \
    NAI_DB_PATH=/var/data/naitiaras.db \
    NAI_COOKIE_SECURE=1
CMD ["python", "backend/server.py"]
