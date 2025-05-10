-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS citasdb;
USE citasdb;

-- Tabla de citas médicas
CREATE TABLE IF NOT EXISTS citas (
    idcita VARCHAR(36) PRIMARY KEY,
    idpaciente VARCHAR(36) NOT NULL,
    iddoctor VARCHAR(36) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    tipo VARCHAR(50) NOT NULL
);

-- Tabla de recetas médicas
CREATE TABLE IF NOT EXISTS recetas (
    idreceta VARCHAR(36) PRIMARY KEY,
    idcita VARCHAR(36) NOT NULL,
    fecha_emision DATE NOT NULL,
    medicamentos TEXT NOT NULL,
    idpaciente VARCHAR(36) NOT NULL,
    iddoctor VARCHAR(36) NOT NULL,
    diagnostico TEXT NOT NULL,
    duracion VARCHAR(100),
    observaciones TEXT,
    requiere_examen_medico BOOLEAN NOT NULL,
    FOREIGN KEY (idcita) REFERENCES citas(idcita)
);
