CREATE TABLE pings(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    url VARCHAR(100),
    ip_address VARCHAR(30),
    datetime DATETIME,
    result BOOLEAN
);
