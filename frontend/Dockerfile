# Use Alpine-based Node image
FROM node:alpine

# Set the working directory
WORKDIR /srv/app

# Install dependencies (You're already in /srv/app)
COPY package.json package-lock.json ./
RUN npm install --silent

# Copy the rest of the code (assuming .dockerignore handles unwanted files)
COPY . .

# Expose the port (default for Vite is 5173)
EXPOSE 5173

# Command to run your application
CMD ["npm", "run", "dev"]