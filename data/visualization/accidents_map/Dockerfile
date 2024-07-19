# Lightest container image to run a NodeJS server.
FROM node:20.8.0-alpine3.17

# Create "datavisualization" working dir in container.
WORKDIR /datavisualization

# Copy NodeJS configuration file in container.
COPY package*.json ./

# Install server dependencies.
RUN npm install

# Copy server source code to container.
COPY . .

# Expose port 3000.
EXPOSE 3000

# Launch server.
CMD npm run dev
