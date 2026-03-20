CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
('Juan Perez', 'juan@example.com'),
('Maria Lopez', 'maria@example.com'),
('Carlos Ruiz', 'carlos@example.com'),
('Ana Torres', 'ana@example.com'),
('Luis Gomez', 'luis@example.com');

INSERT INTO products (name, price, stock) VALUES
('Laptop Dell', 1200.00, 10),
('Monitor LG 24', 300.00, 20),
('Teclado Mecanico', 50.00, 50),
('Mouse Logi', 25.00, 100),
('Silla Ergonomica', 150.00, 15);

INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES
(1, 1, 1, 1200.00),
(2, 2, 2, 600.00),
(3, 3, 1, 50.00),
(4, 4, 3, 75.00),
(5, 5, 2, 300.00);
