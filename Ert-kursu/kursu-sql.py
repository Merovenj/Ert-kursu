# MySQL specific schema definition
mysql_content = """-- MySQL Database Setup Script
CREATE DATABASE IF NOT EXISTS ecom_db;
USE ecom_db;

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO customers (first_name, email) 
VALUES ('John Doe', 'john.doe@example.com');
"""

# Save the commands into a MySQL script file
with open("mysql_schema.sql", "w", encoding="utf-8") as file:
    file.write(mysql_content)

print("MySQL script file 'mysql_schema.sql' generated successfully!")
