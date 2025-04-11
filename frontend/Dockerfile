# Use Node.js version 18.16.0
FROM node:18.16.0

# Create and set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Set npm configurations and install dependencies without optional packages
RUN npm config set fetch-retries 5 \
  && npm config set fetch-retry-mintimeout 20000 \
  && npm config set fetch-retry-maxtimeout 120000 \
  && npm install --no-optional --no-audit --loglevel verbose

# Copy the entire project directory (except for files in .dockerignore)
COPY . .

# Set the environment variable to use legacy OpenSSL provider
ENV NODE_OPTIONS="--openssl-legacy-provider"

# Build the application for production
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]
