# Docker Guide for AI Document Processing System

This guide explains how to run the AI Document Processing System using Docker containers.

## Quick Start

```bash
# Build and start all services
docker-compose up -d

# Process documents
docker-compose exec ai-processor python manage_system.py --process documents/input documents/output

# View logs
docker-compose logs -f
```

## Container Structure

### Services

1. **ai-processor**
   - Main processing service
   - Handles document analysis
   - Runs continuously
   ```bash
   docker-compose up ai-processor
   ```

2. **benchmark**
   - Performance testing service
   - Runs on demand
   ```bash
   docker-compose run benchmark
   ```

3. **diagnostics**
   - System diagnostics service
   - Health monitoring
   ```bash
   docker-compose run diagnostics
   ```

4. **maintenance**
   - Scheduled maintenance
   - Cleanup operations
   ```bash
   docker-compose run maintenance
   ```

## Volume Mounts

```yaml
volumes:
  - ./documents:/app/documents                     # Document storage
  - ./consolidated_documents:/app/consolidated_documents  # Processing output
  - ./logs:/app/logs                              # System logs
  - ./diagnostic_reports:/app/diagnostic_reports   # Diagnostic data
  - ./benchmark_results:/app/benchmark_results     # Performance data
```

## Configuration

### Environment Variables

```yaml
environment:
  - PYTHONUNBUFFERED=1      # Real-time logging
  - PYTHONDONTWRITEBYTECODE=1  # No .pyc files
```

### Resource Limits

```bash
# Set memory limit
docker-compose up -d --memory="4g" ai-processor

# Set CPU limit
docker-compose up -d --cpus="2" ai-processor
```

## Common Operations

### Processing Documents

```bash
# Start processing
docker-compose exec ai-processor python manage_system.py --process input_dir output_dir

# Monitor progress
docker-compose logs -f ai-processor
```

### Running Tests

```bash
# Run all tests
docker-compose run ai-processor python run_tests.py

# Run specific test
docker-compose run ai-processor python -m pytest tests/test_specific.py
```

### Performance Testing

```bash
# Run benchmarks
docker-compose run benchmark

# View results
docker-compose exec ai-processor python view_diagnostic_results.py
```

### System Maintenance

```bash
# Run diagnostics
docker-compose run diagnostics

# Clean up old files
docker-compose run maintenance python cleanup_diagnostics.py
```

## Health Monitoring

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0 if all([os.path.exists(d) for d in ['documents', 'logs']]) else 1)"]
  interval: 30s
  timeout: 30s
  retries: 3
  start_period: 5s
```

### Monitoring Commands

```bash
# Check container status
docker-compose ps

# View health check history
docker inspect ai-processor | grep -A 10 Health

# Monitor resource usage
docker stats ai-processor
```

## Troubleshooting

### Common Issues

1. **Container Won't Start**
   ```bash
   # Check logs
   docker-compose logs ai-processor
   
   # Verify volumes
   docker-compose config
   ```

2. **Processing Errors**
   ```bash
   # Access container
   docker-compose exec ai-processor bash
   
   # Check logs
   tail -f logs/system.log
   ```

3. **Resource Issues**
   ```bash
   # Check resource usage
   docker stats
   
   # Increase limits in docker-compose.yml
   ```

### Debug Mode

```bash
# Start with debug logging
docker-compose run -e DEBUG=1 ai-processor

# Access interactive shell
docker-compose run --entrypoint bash ai-processor
```

## Maintenance

### Updating Images

```bash
# Pull latest base images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Restart with new images
docker-compose up -d --force-recreate
```

### Cleanup

```bash
# Remove stopped containers
docker-compose down

# Clean up volumes
docker-compose down -v

# Remove all related images
docker-compose down --rmi all
```

## Best Practices

1. **Resource Management**
   - Monitor container resources
   - Set appropriate limits
   - Clean up unused containers

2. **Data Persistence**
   - Use named volumes
   - Back up important data
   - Maintain volume permissions

3. **Security**
   - Run as non-root user
   - Limit exposed ports
   - Keep images updated

4. **Performance**
   - Use multi-stage builds
   - Optimize layer caching
   - Monitor resource usage

## Development

### Building Development Image

```bash
# Build with development dependencies
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Testing Changes

```bash
# Run tests in container
docker-compose run ai-processor python run_tests.py

# Check code style
docker-compose run ai-processor black .
```

## Support

For issues or questions:
1. Check container logs
2. Review troubleshooting guide
3. Open GitHub issue
4. Contact support team

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Project Documentation](./README.md)
