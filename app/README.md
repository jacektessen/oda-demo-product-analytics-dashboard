# Redis Service for ODA Dashboard

This component provides caching and data storage functionality for the ODA Dashboard project. It's configured for optimal performance with product data caching and statistics aggregation.

## Quick Start

For installation instructions, see [official Redis documentation](https://redis.io/docs/getting-started/).

### Running Redis

Via Homebrew:
```bash
# Start
brew services start redis

# Stop
brew services stop redis

# Check status
brew services list | grep redis
```

With custom configuration:
```bash
# Start
redis-server redis.conf

# Stop
redis-cli shutdown
```

### Basic Commands

```bash
# Test connection
redis-cli ping

# Check all keys
redis-cli KEYS "*"

# Get specific key value
redis-cli GET key_name

# Monitor Redis operations
redis-cli MONITOR

# Check Redis status
redis-cli INFO
```

## Configuration

Key configuration parameters (see `redis.conf`):
- Memory limit: 256MB
- Cache policy: LRU (Least Recently Used)
- Persistence: RDB snapshots
- Port: 6379
- Log file: `./redis.log`

## Cache Structure

Main key patterns used in the project:
- `products:stats:*` - Product statistics
- `products:categories:*` - Category data
- `products:brands:*` - Brand aggregations
- `cache:*` - General purpose cache

Default TTL for cache entries: 15 minutes

## Troubleshooting

Common issues:
1. Connection refused: Check if Redis is running (`redis-cli ping`)
2. Port conflicts: Check what's using the port (`lsof -i :6379`)
3. Config file errors: Verify paths in `redis.conf` exist
4. Process management: Use `ps aux | grep redis` to check running instances
5. In Docker you can check kyes through e.g. `docker exec -it docker-redis-1 redis-cli`

For more details, refer to [Redis documentation](https://redis.io/documentation).