-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cert;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE cert (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT DEFAULT NULL, 
  description TEXT DEFAULT NULL, 
  serial_number TEXT NOT NULL, 
  valid DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires DATETIME NOT NULL,
  ip VARCHAR(45) NOT NULL,
  uuid VARCHAR(255) NOT NULL, 
  cert_path VARCHAR(255) NOT NULL, 
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

