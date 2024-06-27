-- This script intializes the database hbnb_test_db and the user hbnb_test if neither exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS hbnb_test@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant the appropriate privileges to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO hbnb_test@'localhost';
GRANT SELECT ON performance_schema.* TO hbnb_test@'localhost';
