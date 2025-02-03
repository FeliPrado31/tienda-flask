-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    role ENUM('admin', 'cliente') NOT NULL
);

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de Pedidos
CREATE TABLE IF NOT EXISTS pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'completado') DEFAULT 'pendiente',
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE
);

-- Tabla de Detalles de Pedido
CREATE TABLE IF NOT EXISTS detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE CASCADE
);