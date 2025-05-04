# eYouth Project

## Testing

This project uses pytest for testing, which is configured to run only inside the Docker container.

### Running Tests

To run the tests:

1. Make sure the Docker container is running:
   ```
   docker compose up -d
   ```

2. Execute tests from inside the container:
   ```
   docker exec eyouth-web-1 pytest
   ```

**Important:** Pytest is configured to work only within the Docker environment and will not function correctly when run directly on the host machine. This ensures consistent test execution across different development environments.
