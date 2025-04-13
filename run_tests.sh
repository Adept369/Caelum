#!/bin/bash
# run_tests.sh — Executes your Flask test suite inside Docker (single-personality version)
# Usage: ./run_tests.sh [container_name]
# If no container name is provided, defaults to "adhdpapi-web".

# Exit immediately if a command exits with a non-zero status
set -e

# Optionally rebuild and start containers in detached mode:
docker-compose up --build -d

# Use provided container name or default to "adhdpapi-web"
CONTAINER_NAME=${1:-adhdpapi-web}

echo "🔍 Running Caelum test suite in container: $CONTAINER_NAME..."

# Execute the test suite (using Python's unittest discovery) and log the output to a file.
docker exec -it $CONTAINER_NAME python -m unittest discover -s tests | tee test_output.log

# Check exit code from docker exec via PIPESTATUS to determine test success
if [ ${PIPESTATUS[0]} -eq 0 ]; then
  echo "✅ All tests passed!"
else
  echo "❌ Some tests failed. Review logs above."
fi
