-- RabbitMQ Objects definitions
CREATE TABLE IF NOT EXISTS objects (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cluster_name VARCHAR(128) NOT NULL,
    certificate LONGTEXT NOT NULL,
    filer_id INT NOT NULL UNIQUE,
    server VARCHAR(128) NOT NULL,
    port INT NOT NULL,
    vhost VARCHAR(64) NOT NULL,
    exchange VARCHAR(128) NOT NULL,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(128) NOT NULL,
    UNIQUE (cluster_name),
    UNIQUE (filer_id),
    INDEX IX_cluster_name (cluster_name)
);
