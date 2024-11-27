FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /tests

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy test files
COPY . .

# Install Playwright browsers
RUN npx playwright install --with-deps chromium

# Command to run tests
CMD ["npm", "test"]