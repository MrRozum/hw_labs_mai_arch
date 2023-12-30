CREATE DATABASE IF NOT EXISTS api_db;

USE api_db;

CREATE TABLE IF NOT EXISTS buyer (
  buyer_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  address VARCHAR(200) NOT NULL,
  date_of_birth DATE NOT NULL,
  sex VARCHAR(6) NOT NULL,
  city VARCHAR(50) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  registry_date DATE NOT NULL,
  update_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS company (
  company_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  city VARCHAR(50) NOT NULL,
  address VARCHAR(100) NOT NULL,
  rating NUMERIC,
  phone_number VARCHAR(15) NOT NULL,
  registry_date DATE NOT NULL,
  update_date DATE NOT NULL
);


CREATE TABLE IF NOT EXISTS item_card (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  item_name VARCHAR(100) NOT NULL,
  seller_id INT NOT NULL,
  category_name VARCHAR(100) NOT NULL,
  price NUMERIC NOT NULL,
  rating NUMERIC,
  description TEXT,
  update_date DATE,
  FOREIGN KEY (seller_id) REFERENCES company(company_id)
);


-- Insert default sample data into BUYER table
INSERT INTO 
    buyer (buyer_id, username, password, first_name, last_name, email, address, date_of_birth, sex, city, phone_number, registry_date, update_date) 
VALUES
    (0, 'user1', 'pass1', 'ivan', 'ivanov', 'user1@ml.ru', 'some street1, 1', '2000-12-07', 'male', 'Dubai', '+74758357456', '2023-11-21', '2023-11-21'),
    (0, 'user2', 'pass2', 'ivana', 'ivanova', 'user2@ml.ru', 'some street1, 2', '2002-01-01', 'female', 'Paris', '+78345234985', '2023-04-13', '2023-04-13'),
    (0, 'user3', 'pass3', 'alla', 'ivanova', 'user3@ml.ru', 'some street1, 3', '1998-11-03', 'female', 'York', '+73425234958', '2023-07-05', '2023-07-05'),
    (0, 'user4', 'pass4', 'petr', 'petrov', 'user4@ml.ru', 'some street1, 4', '1994-05-11', 'male', 'Dubai', '+67576234538', '2023-03-15', '2023-03-15'),
    (0, 'user5', 'pass5', 'zurab', 'sidorov', 'user5@ml.ru', 'some street1, 5', '1985-08-12', 'male', 'Dubai', '+75832452873', '2023-01-17', '2023-01-17');


-- Insert default sample data into Company table
INSERT INTO 
    company (company_id, username, password, email, city, address, rating, phone_number, registry_date, update_date) 
VALUES 
    (0, 'some_seller1', 'pass1', 'comp1@ml.ru', 'Berlin', 'berlin street, 2', 4.0, '+73425345958', '2023-01-20', '2023-01-20'),
    (0, 'some_seller2', 'pass2', 'comp2@ml.ru', 'Berlin', 'berlin street, 4', 4.1, '+74523845843', '2023-02-21', '2023-02-21'),
    (0, 'some_seller3', 'pass3', 'comp3@ml.ru', 'Berlin', 'berlin street, 6', 4.2, '+73457238574', '2023-03-22', '2023-03-22'),
    (0, 'some_seller4', 'pass4', 'comp4@ml.ru', 'Berlin', 'berlin street, 8', 4.3, '+78923742783', '2023-04-23', '2023-04-23'),
    (0, 'some_seller5', 'pass5', 'comp5@ml.ru', 'Berlin', 'berlin street, 10', 4.4, '+73495832475', '2023-05-24', '2023-05-24');


INSERT INTO
    item_card (item_id, item_name, seller_id, category_name, price, rating, description, update_date)
VALUES
    (0, 'bosch 2000', 1, 'микровволновка', 15000.00, 4.9, 'Микроволновая печь для самых лучших', '2023-11-25'),
    (0, 'кофемашина 3000', 2, 'кофе', 45000.00, 4.3, 'Варим-варим бодрость мы с утра', '2023-11-25'),
    (0, 'нож кухонный', 3, 'столовые приборы', 1000.00, 3.2, 'Режет как по маслу', '2023-11-25');
