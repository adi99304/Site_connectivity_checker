Below are the sql commands for database:

CREATE DATABASE site_checker;


USE site_checker;


CREATE TABLE checked_sites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    status ENUM('up', 'down') NOT NULL,
    response_time FLOAT,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
drop table checked_sites;
SELECT * FROM checked_sites;


SELECT id, site_name, url, status, response_time, last_checked FROM checked_sites;


SELECT * FROM checked_sites WHERE status = 'up';


SELECT * FROM checked_sites WHERE status = 'down';
