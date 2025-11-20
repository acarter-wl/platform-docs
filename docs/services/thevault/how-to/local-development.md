# Local Development Guide

This guide walks you through setting up Sample Service for local development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 20 or higher
- **npm**: Version 10 or higher
- **Docker Desktop**: For running local dependencies
- **Git**: For version control
- **PostgreSQL Client**: For database access
- **Redis CLI**: For cache debugging (optional)

### Verify Prerequisites

```bash
# Check versions
node --version    # Should be v20.x.x or higher
npm --version     # Should be 10.x.x or higher
docker --version  # Should be 20.x.x or higher
git --version

# Check Docker is running
docker ps
```

## Initial Setup

### 1. Clone the Repository

```bash
# Clone via SSH (recommended)
git clone git@github.com:your-org/sample-service.git
cd sample-service

# Or via HTTPS
git clone https://github.com/your-org/sample-service.git
cd sample-service
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# This will install all packages from package.json
# Might take 2-3 minutes on first run
```

### 3. Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your editor
nano .env
```

Required environment variables:

```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# Database
DATABASE_URL=postgresql://sample_user:sample_pass@localhost:5432/sample_db

# Redis
REDIS_URL=redis://localhost:6379

# External APIs (use test keys)
STRIPE_API_KEY=sk_test_your_test_key
SENDGRID_API_KEY=SG.test_your_test_key

# JWT Secret (generate a random string)
JWT_SECRET=your-super-secret-jwt-key-change-this

# Feature Flags
FEATURE_NEW_UI=true
FEATURE_BETA_API=false
```

### 4. Start Local Dependencies

```bash
# Start PostgreSQL, Redis, and RabbitMQ
docker-compose up -d

# Verify containers are running
docker-compose ps

# Should see:
# - sample-service-postgres
# - sample-service-redis
# - sample-service-rabbitmq
```

### 5. Run Database Migrations

```bash
# Run all migrations
npm run migrate

# You should see output like:
# ✅ Migration 001_create_users_table
# ✅ Migration 002_create_orders_table
# ✅ Migration 003_add_indexes
```

### 6. Seed Database (Optional)

```bash
# Add sample data for development
npm run seed

# This creates:
# - 10 test users
# - 50 sample orders
# - Test products
```

## Running the Application

### Development Mode

```bash
# Start with hot reload
npm run dev

# You should see:
# 🚀 Sample Service started on http://localhost:3000
# 📊 Environment: development
# 🗄️  Database connected
# 💾 Redis connected
```

The server will automatically restart when you make code changes.

### Production Mode (locally)

```bash
# Build TypeScript
npm run build

# Start production server
npm start
```

### Debug Mode

```bash
# Start with debugger attached
npm run debug

# Then attach your IDE debugger to port 9229
```

## Testing Your Setup

### Health Check

```bash
# Test the API is running
curl http://localhost:3000/v1/health

# Expected response:
{
  "status": "healthy",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "queue": "healthy"
  }
}
```

### Create a Test User

```bash
# Register a new user
curl -X POST http://localhost:3000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'

# Expected response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "email": "test@example.com",
    "name": "Test User"
  }
}
```

### Make an Authenticated Request

```bash
# Save the token from previous step
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Get user profile
curl -X GET http://localhost:3000/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

## Running Tests

### Unit Tests

```bash
# Run all unit tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- user.service.test.ts

# Run tests in watch mode
npm test -- --watch
```

### Integration Tests

```bash
# Run integration tests (requires Docker)
npm run test:integration

# This will:
# 1. Start test containers
# 2. Run migrations
# 3. Execute tests
# 4. Clean up
```

### E2E Tests

```bash
# Start the application
npm run dev

# In another terminal, run E2E tests
npm run test:e2e
```

### Linting and Formatting

```bash
# Check code style
npm run lint

# Fix auto-fixable issues
npm run lint:fix

# Format code
npm run format

# Type check
npm run type-check
```

## Database Management

### Access PostgreSQL

```bash
# Connect to database
docker exec -it sample-service-postgres psql -U sample_user -d sample_db

# Or use connection string
psql postgresql://sample_user:sample_pass@localhost:5432/sample_db
```

### Useful SQL Commands

```sql
-- List all tables
\dt

-- Describe table structure
\d users

-- View all users
SELECT * FROM users;

-- Check migration status
SELECT * FROM migrations ORDER BY created_at DESC;

-- Count records
SELECT COUNT(*) FROM orders;
```

### Create a Migration

```bash
# Generate new migration file
npm run migrate:create add_user_preferences

# This creates: migrations/TIMESTAMP_add_user_preferences.sql
```

Edit the migration file:

```sql
-- Up migration
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  theme VARCHAR(20) DEFAULT 'light',
  notifications_enabled BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Down migration (for rollback)
-- DROP TABLE user_preferences;
```

### Run Migration

```bash
# Apply new migration
npm run migrate

# Rollback last migration
npm run migrate:rollback
```

## Redis Management

### Access Redis CLI

```bash
# Connect to Redis
docker exec -it sample-service-redis redis-cli

# Test connection
127.0.0.1:6379> PING
PONG
```

### Useful Redis Commands

```redis
# View all keys
KEYS *

# Get a value
GET session:user-123

# View key info
TTL session:user-123
TYPE session:user-123

# Delete a key
DEL session:user-123

# Clear all cache (careful!)
FLUSHDB
```

### Debug Cache Issues

```bash
# Monitor Redis commands in real-time
docker exec -it sample-service-redis redis-cli MONITOR

# Check cache stats
docker exec -it sample-service-redis redis-cli INFO stats
```

## RabbitMQ Management

### Access Management UI

Open your browser to: http://localhost:15672

- Username: `guest`
- Password: `guest`

### Useful Management Tasks

- View queues and message counts
- Manually publish test messages
- Purge queues during development
- Monitor consumer connections

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-user-preferences

# Push to remote
git push -u origin feature/add-user-preferences
```

### 2. Make Changes

```bash
# Edit code
code src/services/user-preferences.service.ts

# Run tests as you develop
npm test -- --watch

# Check code style
npm run lint
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add user preferences endpoint"

# Commit message format:
# - feat: New feature
# - fix: Bug fix
# - docs: Documentation changes
# - refactor: Code refactoring
# - test: Test changes
# - chore: Build/tooling changes
```

### 4. Push and Create PR

```bash
# Push to remote
git push

# Create PR via GitHub UI or CLI
gh pr create --title "Add user preferences" --body "Implements user preferences endpoint"
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
PORT=3001 npm run dev
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Restart database
docker-compose restart postgres

# View database logs
docker logs sample-service-postgres

# Verify connection string in .env
echo $DATABASE_URL
```

### Redis Connection Failed

```bash
# Check Redis is running
docker ps | grep redis

# Restart Redis
docker-compose restart redis

# Test connection
redis-cli -h localhost -p 6379 ping
```

### Module Not Found

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear npm cache
npm cache clean --force
```

### TypeScript Errors

```bash
# Rebuild TypeScript
npm run build

# Check for type errors
npm run type-check

# Clear build cache
rm -rf dist/
npm run build
```

### Tests Failing

```bash
# Reset test database
npm run test:db:reset

# Clear Jest cache
npm test -- --clearCache

# Run specific test file
npm test -- user.service.test.ts --verbose
```

### Docker Issues

```bash
# Stop all containers
docker-compose down

# Remove volumes and start fresh
docker-compose down -v
docker-compose up -d

# View container logs
docker-compose logs postgres
docker-compose logs redis

# Restart all services
docker-compose restart
```

## IDE Setup

### VS Code

Recommended extensions:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "orta.vscode-jest",
    "christian-kohler.path-intellisense",
    "usernamehw.errorlens"
  ]
}
```

Debug configuration (`.vscode/launch.json`):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug App",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "debug"],
      "port": 9229,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### IntelliJ IDEA

1. Open project directory
2. Right-click `package.json` → Show npm Scripts
3. Double-click scripts to run them
4. Configure run configurations for debugging

## Useful Commands Reference

```bash
# Development
npm run dev          # Start dev server with hot reload
npm run build        # Build TypeScript
npm start            # Start production server
npm run debug        # Start with debugger

# Testing
npm test             # Run unit tests
npm run test:watch   # Run tests in watch mode
npm run test:cov     # Run with coverage
npm run test:int     # Run integration tests
npm run test:e2e     # Run E2E tests

# Code Quality
npm run lint         # Check code style
npm run lint:fix     # Fix auto-fixable issues
npm run format       # Format with Prettier
npm run type-check   # TypeScript type checking

# Database
npm run migrate      # Run migrations
npm run migrate:rollback  # Rollback last migration
npm run seed         # Seed database

# Docker
docker-compose up -d       # Start services
docker-compose down        # Stop services
docker-compose logs -f     # Follow logs
docker-compose ps          # List containers
```

## Getting Help

- **Documentation**: Check this docs site
- **Slack**: #sample-service-dev channel
- **Code Review**: Tag team members on PR
- **Architecture Questions**: #architecture channel
- **Bugs**: Create GitHub issue with label `bug`

## Next Steps

- [API Documentation](../api/endpoints.md) - Learn about available endpoints
- [Architecture Overview](../architecture/overview.md) - Understand system design
- [Contributing Guide](https://github.com/your-org/sample-service/blob/main/CONTRIBUTING.md) - Coding standards
- [Runbooks](../runbooks/incident-response.md) - Operational procedures
