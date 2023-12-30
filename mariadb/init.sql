CREATE DATABASE IF NOT EXISTS api_db;

USE api_db;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  is_seller BOOLEAN NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Create ProductCards table
CREATE TABLE IF NOT EXISTS ProductCards (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  seller_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  category VARCHAR(50) NOT NULL,
  price DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (seller_id) REFERENCES Users(user_id)
);


-- Create PurchaseHistory table
CREATE TABLE IF NOT EXISTS PurchaseHistory (
    purchase_id INT PRIMARY KEY AUTO_INCREMENT,
    buyer_id INT,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id)
);


-- Create PurchaseItems table
CREATE TABLE IF NOT EXISTS PurchaseItems (
    purchase_item_id INT PRIMARY KEY AUTO_INCREMENT,
    purchase_id INT,
    product_id INT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES PurchaseHistory(purchase_id),
    FOREIGN KEY (product_id) REFERENCES ProductCards(product_id)
);

-- Create ItemCart table
CREATE TABLE IF NOT EXISTS ItemCart(
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY(user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES ProductCards(product_id)
);



-- Insert Sample Users
INSERT INTO Users (username, password, first_name, last_name, email, is_seller)
VALUES ('seller1', 'password1', 'John', 'Doe', 'john@example.com', TRUE),
       ('buyer1', 'password2', 'Alice', 'Smith', 'alice@example.com', FALSE),
       ('bobovich', 'bobeno', 'Bob', 'Bobovich', 'bobovich@mai.edu', FALSE),
       ('vjobovich', 'vjobe', 'Varliy', 'Jobovich', 'vjobovich@na.edu', TRUE);

-- Insert Sample ProductCards
INSERT INTO ProductCards (seller_id, title, description, category, price)
VALUES (1, 'Product 1', 'Description for Product 1', 'Category A', 29.99),
       (1, 'Product 2', 'Description for Product 2', 'Category B', 49.99),
       (1, 'Product 3', 'Description for Product 3', 'Category A', 39.99),
       (4, 'Vagu', 'Tasty premium meat', 'Meat', 1500.29),
       (4, 'Pork', 'Tasty affordable meat', 'Meat', 1500.29);