-- Створення таблиці користувачів
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Створення таблиці квітів
CREATE TABLE flowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Створення таблиці голосів
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    user_login VARCHAR(150) NOT NULL,
    first_choice INTEGER NOT NULL,
    second_choice INTEGER NOT NULL,
    third_choice INTEGER NOT NULL,
    FOREIGN KEY (user_login) REFERENCES users(username),
    FOREIGN KEY (first_choice) REFERENCES flowers(id),
    FOREIGN KEY (second_choice) REFERENCES flowers(id),
    FOREIGN KEY (third_choice) REFERENCES flowers(id)
);

-- Наповнення таблиці квітів 20 екземплярами
INSERT INTO flowers (name) VALUES
('Троянда'),
('Лілія'),
('Ромашка'),
('Тюльпан'),
('Нарцис'),
('Орхідея'),
('Гвоздика'),
('Півонія'),
('Айстра'),
('Фіалка'),
('Хризантема'),
('Ірис'),
('Бузок'),
('Кульбаба'),
('Мак'),
('Жоржина'),
('Лаванда'),
('Мальва'),
('Соняшник'),
('Камелія');
