CREATE DATABASE IF NOT EXISTS staging_db;

USE staging_db; 

DROP TABLE IF EXISTS to_do;

CREATE TABLE to do (
    task_id INT AUTO_INCREMENT PRIMARY KEY, 
    task VARCHAR(120) NOT NULL,
    task_status VARCHAR(120) NOT NULL default 'PENDING'
);