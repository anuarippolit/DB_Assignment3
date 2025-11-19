DROP TABLE IF EXISTS APPOINTMENT CASCADE;
DROP TABLE IF EXISTS JOB_APPLICATION CASCADE;
DROP TABLE IF EXISTS JOB CASCADE;
DROP TABLE IF EXISTS ADDRESS CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS CAREGIVER CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;

CREATE TABLE "USER" (
    user_id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    given_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    city TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    profile_description TEXT,
    password TEXT NOT NULL
);

CREATE TABLE CAREGIVER (
    caregiver_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    photo TEXT,
    gender TEXT NOT NULL,
    caregiving_type TEXT NOT NULL CHECK (caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    hourly_rate DECIMAL(6, 2) NOT NULL CHECK (hourly_rate >= 0)
);

CREATE TABLE MEMBER (
    member_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    house_rules TEXT,
    dependent_description TEXT
);

CREATE TABLE ADDRESS (
    member_user_id INTEGER PRIMARY KEY REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
    house_number TEXT NOT NULL,
    street TEXT NOT NULL,
    town TEXT NOT NULL
);

CREATE TABLE JOB (
    job_id INTEGER PRIMARY KEY,
    member_user_id INTEGER NOT NULL REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
    required_caregiving_type TEXT NOT NULL CHECK (required_caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    other_requirements TEXT,
    date_posted DATE NOT NULL
);

CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INTEGER NOT NULL REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES JOB(job_id) ON DELETE CASCADE,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id)
);

CREATE TABLE APPOINTMENT (
    appointment_id INTEGER PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    member_user_id INTEGER NOT NULL REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours INTEGER NOT NULL CHECK (work_hours > 0),
    status TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'declined'))
);


INSERT INTO "USER" (user_id, email, given_name, surname, city, phone_number, profile_description, password) VALUES
(1, 'anuar.akimbekov@gmail.com', 'Anuar', 'Akimbekov', 'Astana', '+7707 111 11 11', 'Experienced caregiver with 5 years in elderly care', 'password123'),
(2, 'pavel.kokoshko@nu.edu.kz', 'Pavel', 'Kokoshko', 'Almaty', '+7 707 222 22 22', 'Professional babysitter, certified in child care', 'password123'),
(3, 'anna.kazakhstan@gmail.com', 'Anna', 'Kazakhstan', 'Astana', '+7707 333 33 33', 'Creative playmate, loves arts and crafts', 'password123'),
(4, 'max.verstappen@gmail.com', 'Max', 'Verstappen', 'Shymkent', '+7707 444 44 44', 'Compassionate caregiver specializing in elderly care', 'password123'),
(5, 'lewis.hamilton@nu.edu.kz', 'Lewis', 'Hamilton', 'Astana', '+7707 555 55 55', 'Reliable babysitter, I had early childhood education background', 'password123'),
(6, 'zarina.nurmanova@mail.ru', 'Zarina', 'Nurmanova', 'Astana', '+7707 666 66 66', 'Experienced in both babysitting and elderly care', 'password123'),
(7, 'dilnaz.serikova@nu.edu.kz', 'Dilnaz', 'Serikova', 'Astana', '+7707 777 77 77', 'Professional elderly care specialist', 'password123'),
(8, 'aida.nurpeisova@gmail.com', 'Aida', 'Nurpeisova', 'Astana', '+7707 888 88 88', 'I am good caregiver', 'password123'),
(9, 'madina.alimova@mail.ru', 'Madina', 'Alimova', 'Astana', '+7707 999 99 99', 'Specialist in dementia care', 'password123'),
(10, 'ayana.zhaksybekova@nu.edu.kz', 'Ayana', 'Zhaksybekova', 'Astana', '+7707 123 45 67', 'Professional caregiver available weekends', 'password123'),
(11, 'arman.armanov@nu.edu.kz', 'Arman', 'Armanov', 'Astana', '+7707 987 65 43', 'Caregiver profile', 'password123'),
(12, 'ignat.ippolitovich@mail.ru', 'Ignat', 'Ippolitovich', 'Astana', '+7707 111 22 22', 'Father of two young children', 'password123'),
(13, 'innokentiya.ippolitovich@gmail.com', 'Innokentiya', 'Ippolitovich', 'Almaty', '+7707 222 33 33', 'Looking for caregiver for elderly mother', 'password123'),
(14, 'kondratiya.ippolitovich@nu.edu.kz', 'Kondratiya', 'Ippolitovich', 'Astana', '+7707 333 44 44', 'Single father, needs reliable childcare', 'password123'),
(15, 'gulnara.gulimova@mail.ru', 'Gulnara', 'Gulimova', 'Astana', '+7707 444 55 55', 'Working mother needing weekend care', 'password123'),
(16, 'aigerim.nurlanova@gmail.com', 'Aigerim', 'Nurlanova', 'Almaty', '+7707 555 66 66', 'Daughter caring for aging parent', 'password123'),
(17, 'asel.mukhanova@nu.edu.kz', 'Asel', 'Mukhanova', 'Astana', '+7707 666 77 77', 'Mother of special needs child', 'password123'),
(18, 'carlos.sainz@mail.ru', 'Carlos', 'Sainz', 'Astana', '+7707 777 88 88', 'Working professional, needs flexible care', 'password123'),
(19, 'roza.raimbaeva@gmail.com', 'Roza', 'Raimbaeva', 'Astana', '+7707 888 99 99', 'Grandmother watching grandchildren', 'password123'),
(20, 'george.russel@nu.edu.kz', 'George', 'Russel', 'Astana', '+7707 999 11 11', 'Elderly care needed for homebound relative', 'password123'),
(21, 'valtteri.bottas@mail.ru', 'Valtteri', 'Bottas', 'Astana', '+7707 123 98 76', 'Busy professional parent', 'password123'),
(22, 'amina.aminova@gmail.com', 'Amina', 'Aminova', 'Almaty', '+7707 987 12 34', 'Member profile', 'password123');

INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'photo1.jpg', 'Male', 'elderly care', 1500.00),
(2, 'photo2.jpg', 'Male', 'babysitter', 1200.00),
(3, 'photo3.jpg', 'Female', 'playmate for children', 1000.00),
(4, 'photo4.jpg', 'Male', 'elderly care', 1800.00),
(5, 'photo5.jpg', 'Male', 'babysitter', 1100.00),
(6, 'photo6.jpg', 'Female', 'elderly care', 1600.00),
(7, 'photo7.jpg', 'Female', 'elderly care', 2000.00),
(8, 'photo8.jpg', 'Female', 'elderly care', 1700.00),
(9, 'photo9.jpg', 'Female', 'elderly care', 2100.00),
(10, 'photo10.jpg', 'Female', 'elderly care', 2200.00),
(11, 'photo11.jpg', 'Male', 'babysitter', 3800.00);

INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(12, 'No pets. Please maintain cleanliness. Quiet environment preferred.', 'I have a 5-year old son who likes painting and reading.'),
(13, 'No pets. Please follow medication schedule strictly.', 'Elderly mother, 78 years old, needs assistance with daily activities.'),
(14, 'No smoking. Please be punctual.', 'Two children: 7-year-old daughter and 4-year-old son.'),
(15, 'No pets. Flexible schedule required.', 'Two children, 8 and 10 years old, need weekend supervision.'),
(16, 'No pets. Must be certified in elderly care.', 'Aging parent, 82 years old, requires 24/7 monitoring.'),
(17, 'No pets. Must have experience with special needs.', 'Special needs child, 6 years old, requires specialized care.'),
(18, 'No pets. Flexible hours preferred.', 'Working professional, needs flexible care for elderly relative.'),
(19, 'No pets. Please maintain quiet environment.', 'Watching three grandchildren, ages 3, 5, and 7.'),
(20, 'No pets. Homebound care required.', 'Elderly relative, homebound, needs daily assistance.'),
(21, 'No pets. Busy schedule, need reliable caregiver.', 'Working professional with two children, ages 4 and 7.'),
(22, 'No pets. Regular schedule required.', 'Elderly parent, 75 years old, needs daily assistance.');

INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
(12, '45', 'Kabanbay Batyr', 'Astana'),
(13, '123', 'Abay Avenue', 'Almaty'),
(14, '78', 'Kabanbay Batyr', 'Astana'),
(15, '12', 'Nazarbayev Avenue', 'Astana'),
(16, '234', 'Dostyk Avenue', 'Almaty'),
(17, '56', 'Kabanbay Batyr', 'Astana'),
(18, '34', 'Saryarka Avenue', 'Astana'),
(19, '67', 'Kabanbay Batyr', 'Astana'),
(20, '78', 'Kabanbay Batyr', 'Astana'),
(21, '101', 'Auezov Avenue', 'Astana'),
(22, '55', 'Al-Farabi Avenue', 'Almaty');

INSERT INTO JOB (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(1, 13, 'elderly care', 'Must be soft-spoken and patient. Certification required.', '2025-01-15'),
(2, 12, 'babysitter', 'Experience with arts and crafts preferred.', '2025-01-20'),
(3, 14, 'babysitter', 'Must be reliable and punctual. CPR certified.', '2025-02-01'),
(4, 16, 'elderly care', 'Looking for soft-spoken caregiver with experience in dementia care.', '2025-02-10'),
(5, 15, 'playmate for children', 'Creative activities preferred. Weekend availability.', '2025-02-15'),
(6, 17, 'babysitter', 'Special needs experience required. Must be patient and soft-spoken.', '2025-02-20'),
(7, 18, 'elderly care', 'Flexible schedule. Must be soft-spoken and understanding.', '2025-03-01'),
(11, 20, 'elderly care', 'Homebound care. Must be soft-spoken and compassionate.', '2025-03-15'),
(12, 21, 'babysitter', 'Professional caregiver needed. Reliable schedule.', '2025-03-20'),
(13, 13, 'elderly care', 'Part-time position. Soft-spoken personality required.', '2025-04-01'),
(14, 16, 'elderly care', 'Full-time elderly care specialist needed.', '2025-04-05'),
(15, 18, 'elderly care', 'Weekend availability. Must be gentle and soft-spoken.', '2025-04-10'),
(16, 22, 'elderly care', 'Full-time position. Must be certified.', '2025-04-12'),
(17, 22, 'babysitter', 'Part-time evening care needed.', '2025-04-15'),
(18, 22, 'playmate for children', 'Weekend activities preferred.', '2025-04-18');

INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2025-01-16'),
(1, 4, '2025-02-11'),
(1, 7, '2025-03-02'),
(1, 11, '2025-03-16'),
(4, 1, '2025-01-17'),
(4, 4, '2025-02-12'),
(6, 1, '2025-01-18'),
(6, 7, '2025-03-03'),
(7, 1, '2025-01-19'),
(7, 4, '2025-02-13'),
(7, 11, '2025-03-17'),
(8, 7, '2025-03-04'),
(8, 13, '2025-04-02'),
(9, 1, '2025-01-21'),
(9, 4, '2025-02-15'),
(9, 11, '2025-03-18'),
(10, 7, '2025-03-05'),
(10, 13, '2025-04-03'),
(2, 2, '2025-01-21'),
(2, 3, '2025-02-02'),
(5, 2, '2025-01-22'),
(5, 6, '2025-03-06'),
(3, 5, '2025-02-16'),
(11, 2, '2025-01-23'),
(11, 3, '2025-02-04');

INSERT INTO APPOINTMENT (appointment_id, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 1, 13, '2025-05-01', '09:00:00', 3, 'accepted'),
(2, 1, 16, '2025-05-02', '10:00:00', 4, 'accepted'),
(3, 4, 13, '2025-05-03', '14:00:00', 5, 'accepted'),
(4, 6, 18, '2025-05-04', '09:00:00', 4, 'accepted'),
(5, 7, 13, '2025-05-05', '11:00:00', 4, 'accepted'),
(6, 8, 16, '2025-05-06', '13:00:00', 6, 'accepted'),
(7, 11, 18, '2025-05-07', '10:00:00', 3, 'accepted'),
(8, 9, 13, '2025-05-08', '15:00:00', 5, 'accepted'),
(9, 10, 16, '2025-05-09', '09:00:00', 5, 'accepted'),
(10, 1, 18, '2025-05-10', '12:00:00', 3, 'accepted'),
(11, 2, 12, '2025-05-11', '09:00:00', 4, 'pending'),
(12, 5, 14, '2025-05-12', '10:00:00', 4, 'pending'),
(13, 11, 15, '2025-05-13', '14:00:00', 5, 'declined'),
(14, 2, 12, '2025-05-14', '11:00:00', 4, 'pending'),
(15, 3, 17, '2025-05-15', '13:00:00', 6, 'accepted'),
(16, 4, 15, '2025-05-16', '15:00:00', 3, 'accepted'),
(17, 5, 14, '2025-05-17', '09:00:00', 5, 'accepted'),
(18, 6, 21, '2025-05-18', '10:00:00', 3, 'pending'),
(19, 7, 18, '2025-05-19', '12:00:00', 5, 'accepted'),
(20, 9, 20, '2025-05-20', '14:00:00', 4, 'accepted');