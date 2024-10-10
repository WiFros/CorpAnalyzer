# Step 1: Build stage using Node.js
FROM node:20.15.1-alpine3.20 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Step 2: Production stage
FROM node:20.15.1-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Install 'serve' to serve the static files
RUN npm install -g serve

# Copy the build output from the 'build' stage
COPY --from=build /app/dist /app/build

# Expose the port that the app will run on (e.g., 3000)
EXPOSE 3000

# Start the static file server using 'serve'
CMD ["serve", "-s", "build", "-l", "3000"]
