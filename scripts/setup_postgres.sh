#!/bin/bash
# PostgreSQL Setup Script for Task Tracker
# This script requires sudo access and should be run by an administrator

set -e

echo "Setting up PostgreSQL for Task Tracker..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Installing PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib

    # Start and enable PostgreSQL service
    sudo systemctl start postgresql
    sudo systemctl enable postgresql

    echo "PostgreSQL installed and started successfully."
else
    echo "PostgreSQL is already installed."
fi

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql -f "$(dirname "$0")/init_postgres.sql"

# Set up environment variables file
ENV_FILE="/etc/task-tracker/postgres.env"
echo "Creating environment configuration..."
sudo mkdir -p "$(dirname "$ENV_FILE")"
sudo tee "$ENV_FILE" > /dev/null << EOF
# PostgreSQL configuration for Task Tracker
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=task_tracker
export POSTGRES_USER=task_tracker_user
export POSTGRES_PASSWORD=change_this_password
EOF

echo ""
echo "PostgreSQL setup completed successfully!"
echo ""
echo "IMPORTANT: Update the password in $ENV_FILE"
echo ""
echo "To use PostgreSQL backend:"
echo "  source $ENV_FILE"
echo "  task-tracker --backend postgresql <command>"
echo ""
echo "To run tests with PostgreSQL:"
echo "  export POSTGRES_TEST_HOST=localhost"
echo "  export POSTGRES_TEST_DB=task_tracker_test"
echo "  export POSTGRES_TEST_USER=task_tracker_user"
echo "  export POSTGRES_TEST_PASSWORD=change_this_password"
echo "  pytest tests/test_postgres_store.py"