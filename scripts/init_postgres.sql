-- PostgreSQL Database Schema for Task Tracker
-- Run this script as postgres user to set up the database

-- Create database
CREATE DATABASE task_tracker;

-- Create user
CREATE USER task_tracker_user WITH PASSWORD 'change_this_password';

-- Connect to the task_tracker database
\c task_tracker;

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high'))
);

-- Create indexes for better performance
CREATE INDEX idx_tasks_done ON tasks (done);
CREATE INDEX idx_tasks_priority ON tasks (priority);
CREATE INDEX idx_tasks_created_at ON tasks (created_at);

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE task_tracker TO task_tracker_user;
GRANT ALL PRIVILEGES ON TABLE tasks TO task_tracker_user;
GRANT USAGE, SELECT ON SEQUENCE tasks_id_seq TO task_tracker_user;

-- Insert sample data (optional)
INSERT INTO tasks (title, priority) VALUES
    ('Setup PostgreSQL backend', 'high'),
    ('Write documentation', 'medium'),
    ('Add unit tests', 'medium'),
    ('Deploy to production', 'low');

-- Display setup confirmation
SELECT 'PostgreSQL setup completed successfully!' as status;
SELECT COUNT(*) as sample_tasks_created FROM tasks;