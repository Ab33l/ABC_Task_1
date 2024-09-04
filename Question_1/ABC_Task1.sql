CREATE DATABASE ABC_Task1;

\c DAC;

CREATE TABLE owners (
    owner_id SERIAL PRIMARY KEY,
    owner_fname VARCHAR(100),
    email_address VARCHAR(255)
);

CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES owners(owner_id),
    car_model VARCHAR(100),
    car_registration_number VARCHAR(50)
);

CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(vehicle_id),
    service_type VARCHAR(100),
    service_date DATE,
    cost NUMERIC(10, 2)
);

INSERT INTO owners (owner_fname, email_address) VALUES
('Adam Elijah', 'adam.elijah@google.com'),
('Elisha Amos', 'elisha.amos@google.com'),
('Alice Jane', 'alice.jane@google.com'),
('Samson Peter', 'samson.peter@google.com');

INSERT INTO vehicles (owner_id, car_model, car_registration_number) VALUES
(1, 'Toyota Corolla', 'KAS 123H'),
(1, 'Honda Civic', 'KCA 213P'),
(2, 'Ford Focus', 'KDM 985F'),
(3, 'Mercedes G63', 'KCC 612B'),
(4, 'BMW i8', 'KDB 105E');

INSERT INTO services (vehicle_id, service_type, service_date, cost) VALUES
(1, 'Oil Change', '2024-01-15', 5000.10),
(1, 'Tire Rotation', '2024-02-20', 1230.25),
(2, 'Brake Inspection', '2024-03-10', 17289.09),
(3, 'Battery Replacement', '2024-04-05', 1020.70),
(4, 'Engine Tune-Up', '2024-05-12', 1500.00),
(5, 'Transmission Repair', '2024-06-18', 6321.00),
(1, 'Air Filter Replacement', '2024-07-22', 2500.00),
(2, 'Wheel Alignment', '2024-08-30', 8345.10);
