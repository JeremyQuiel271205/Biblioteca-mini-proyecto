CREATE SCHEMA biblioteca;

USE biblioteca;

CREATE TABLE usuario(
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE estudiante(
    id_estudiante INT PRIMARY KEY,
    becado BOOLEAN DEFAULT FALSE,
    carrera VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE profesor(
    id_profesor INT PRIMARY KEY,
    asignatura VARCHAR(50) NOT NULL,
    salario_mensual DECIMAL(10,2) NOT NULL DEFAULT 100000.00,
    FOREIGN KEY (id_profesor) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE libro(
    id_libro INT PRIMARY KEY AUTO_INCREMENT,
    nombre_libro VARCHAR(100) NOT NULL,
    nombre_autor VARCHAR(50) NOT NULL,
    apellido_autor VARCHAR(50) NOT NULL DEFAULT '',
    precio_base DECIMAL(9,2) NOT NULL
);


CREATE TABLE prestamo(
    id_prestamo INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    estado ENUM('activo', 'vencido', 'devuelto', 'cancelado') NOT NULL DEFAULT 'activo',
    fecha_ini DATE NOT NULL DEFAULT (CURDATE()),
    fecha_fin DATE NOT NULL,
    interes_dia DECIMAL(9,2) NOT NULL DEFAULT 1500.00 -- lo que se cobra por cada dia de retraso
);

CREATE TABLE notificacion(
    id_notificacion INT PRIMARY KEY AUTO_INCREMENT,
    correo_de VARCHAR(100) NOT NULL,
    correo_para VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mensaje TEXT NOT NULL
);

ALTER TABLE usuario ADD COLUMN contra VARCHAR(100) NOT NULL;