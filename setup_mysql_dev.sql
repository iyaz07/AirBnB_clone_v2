-- This script intializes the database hbnb_dev_db and the user hbnb_dev if neither exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS hbnb_dev@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant the appropriate privileges to hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO hbnb_dev@'localhost';
GRANT SELECT ON performance_schema.* TO hbnb_dev@'localhost';
