# Simple Node-based build and serve
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build argument for API URL
ARG VITE_API_URL=http://localhost:8080
ENV VITE_API_URL=${VITE_API_URL}

# Build the application
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

# Expose port 80
EXPOSE 80

# Serve the built application
CMD ["serve", "-s", "dist", "-l", "80"]

