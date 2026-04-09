# PostgreSQL Setup Documentation

## Installation Attempt Result

**Status**: ❌ Permission Denied

Attempted to install PostgreSQL using:
```bash
sudo apt install postgresql
```

**Error**: Permission to use Bash with command `sudo apt update` has been denied.

## Required System Setup (for Administrator)

To enable PostgreSQL support, a system administrator needs to:

1. Install PostgreSQL server:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. Create database and user:
   ```bash
   sudo -u postgres createdb task_tracker
   sudo -u postgres createuser --interactive task_tracker_user
   ```

3. Set up authentication (optional, for production):
   ```bash
   sudo -u postgres psql
   ALTER USER task_tracker_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE task_tracker TO task_tracker_user;
   ```

## Application Configuration

Once PostgreSQL is installed, the application supports both JSON file and PostgreSQL backends:

- **JSON Backend** (default): `task-tracker --backend=json`
- **PostgreSQL Backend**: `task-tracker --backend=postgresql`

## Environment Variables

For PostgreSQL backend, set these environment variables:
```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=task_tracker
export POSTGRES_USER=task_tracker_user
export POSTGRES_PASSWORD=secure_password
```

## Schema

The PostgreSQL schema is automatically created when first connecting:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    priority VARCHAR(10) DEFAULT 'medium'
);
```