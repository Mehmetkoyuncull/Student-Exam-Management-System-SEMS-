/* ======================================== */
/* DATABASE CREATION                        */
/* ======================================== */

DROP DATABASE IF EXISTS StudentExamDB;
CREATE DATABASE StudentExamDB;
USE StudentExamDB;

/* ======================================== */
/* TABLE DEFINITIONS                        */
/* ======================================== */

CREATE TABLE Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    registration_date DATE NOT NULL
);

CREATE TABLE Instructor (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_last_name VARCHAR(100) NOT NULL,
    title VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100)
);

CREATE TABLE Course (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    credit INT NOT NULL,
    department VARCHAR(100)
);

CREATE TABLE Term (
    term_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE CourseOffering (
    offer_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    term_id INT NOT NULL,
    instructor_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (term_id) REFERENCES Term(term_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
);

CREATE TABLE Registration (
    registration_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    offer_id INT NOT NULL,
    registration_date DATE NOT NULL,
    status VARCHAR(20),
    UNIQUE (student_id, offer_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (offer_id) REFERENCES CourseOffering(offer_id)
);

CREATE TABLE Exam (
    exam_id INT PRIMARY KEY AUTO_INCREMENT,
    offer_id INT NOT NULL,
    exam_type ENUM('midterm','final','quiz') NOT NULL,
    exam_date DATE NOT NULL,
    weight INT NOT NULL CHECK (weight BETWEEN 0 AND 100),
    FOREIGN KEY (offer_id) REFERENCES CourseOffering(offer_id)
);

CREATE TABLE ExamResult (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    exam_id INT NOT NULL,
    student_id INT NOT NULL,
    score INT CHECK (score BETWEEN 0 AND 100),
    pass_flag BOOLEAN,
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

/* ======================================== */
/* SAMPLE DATA INSERTIONS                   */
/* ======================================== */

INSERT INTO Student (first_last_name, email, department, registration_date) VALUES
('Mehmet Koyuncu','mehmet.koyuncu@stu.edu','Computer Engineering','2023-09-01'),
('Mustafa Oz','mustafa.oz@stu.edu','Computer Engineering','2023-09-01'),
('Ahmet Demir','ahmet.demir@stu.edu','Software Engineering','2022-09-05'),
('Ayse Yilmaz','ayse.yilmaz@stu.edu','Computer Engineering','2021-09-10'),
('Fatma Kara','fatma.kara@stu.edu','Information Systems','2024-02-01'),
('Elif Aydin','elif.aydin@stu.edu','Computer Engineering','2023-02-10'),
('Hakan Celik','hakan.celik@stu.edu','Software Engineering','2022-10-21'),
('Zeynep Er','zeynep.er@stu.edu','Computer Engineering','2021-09-07'),
('Baran Ucar','baran.ucar@stu.edu','Information Systems','2023-05-15'),
('Cagla Ari','cagla.ari@stu.edu','Computer Engineering','2023-02-20'),
('Berk Atay','berk.atay@stu.edu','Software Engineering','2024-01-10'),
('Deniz Can','deniz.can@stu.edu','Computer Engineering','2023-09-01');

INSERT INTO Instructor (first_last_name, title, email, department) VALUES
('Bahman Arasteh','Assoc. Prof.','bahman.arasteh@unl.edu','Software Engineering'),
('Seda Yildiz','Dr.','seda.yildiz@unl.edu','Computer Engineering'),
('Mert Aksoy','Dr.','mert.aksoy@unl.edu','Computer Engineering'),
('Gokce Sahin','Prof. Dr.','gokce.sahin@unl.edu','Information Systems'),
('Efe Yalcin','Dr.','efe.yalcin@unl.edu','Software Engineering'),
('Kerem Ince','Asst. Prof.','kerem.ince@unl.edu','Computer Engineering'),
('Nazan Korkmaz','Dr.','nazan.korkmaz@unl.edu','Software Engineering'),
('Huseyin Ates','Assoc. Prof.','huseyin.ates@unl.edu','Computer Engineering'),
('Sinem Ali','Dr.','sinem.ali@unl.edu','Information Systems'),
('Onur Tas','Dr.','onur.tas@unl.edu','Computer Engineering');

INSERT INTO Course (code, name, credit, department) VALUES
('CSE101','Introduction to Programming',6,'Computer Engineering'),
('CSE102','Data Structures',6,'Computer Engineering'),
('CSE201','Database Management Systems',5,'Software Engineering'),
('CSE202','Operating Systems',5,'Computer Engineering'),
('CSE203','Algorithms',6,'Computer Engineering'),
('CSE204','Web Development',5,'Software Engineering'),
('CSE205','Computer Networks',5,'Computer Engineering'),
('CSE301','Machine Learning',6,'Computer Engineering'),
('CSE302','Artificial Intelligence',6,'Software Engineering'),
('CSE303','Mobile App Development',5,'Software Engineering'),
('CSE304','Cloud Computing',5,'Information Systems'),
('CSE305','Cyber Security',6,'Computer Engineering');

INSERT INTO Term (name,start_date,end_date) VALUES
('Fall 2023','2023-09-01','2023-12-30'),
('Spring 2024','2024-02-01','2024-06-01'),
('Fall 2024','2024-09-01','2024-12-30'),
('Spring 2023','2023-02-01','2023-06-01'),
('Fall 2025','2025-09-01','2025-12-30'),
('Spring 2025','2025-02-01','2025-06-01');

INSERT INTO CourseOffering (course_id,term_id,instructor_id,start_date,end_date) VALUES
(1,1,1,'2023-09-10','2023-12-20'),
(2,1,2,'2023-09-12','2023-12-22'),
(3,2,1,'2024-02-05','2024-05-25'),
(4,2,3,'2024-02-07','2024-05-28'),
(5,1,2,'2023-09-11','2023-12-21'),
(6,2,4,'2024-02-10','2024-05-30'),
(7,3,6,'2024-09-05','2024-12-20'),
(8,3,7,'2024-09-07','2024-12-23'),
(9,3,8,'2024-09-12','2024-12-27'),
(10,4,5,'2023-02-08','2023-05-26'),
(11,3,10,'2024-09-10','2024-12-22'),
(12,1,9,'2023-09-15','2023-12-25');

INSERT INTO Registration (student_id,offer_id,registration_date,status) VALUES
(1,1,'2023-09-05','registered'),
(2,1,'2023-09-06','registered'),
(3,1,'2023-09-06','registered'),
(1,2,'2023-09-07','registered'),
(4,2,'2023-09-07','registered'),
(5,2,'2023-09-07','registered'),
(6,3,'2024-02-10','registered'),
(7,3,'2024-02-11','registered'),
(8,4,'2024-02-11','registered'),
(9,4,'2024-02-12','registered'),
(10,5,'2023-09-10','registered'),
(11,6,'2024-02-15','registered'),
(12,6,'2024-02-16','registered'),
(1,7,'2024-09-05','registered'),
(2,7,'2024-09-05','registered');

INSERT INTO Exam (offer_id,exam_type,exam_date,weight) VALUES
(1,'midterm','2023-11-01',40),
(1,'final','2023-12-20',60),
(2,'midterm','2023-11-05',50),
(2,'final','2023-12-22',50),
(3,'quiz','2024-03-01',20),
(3,'final','2024-05-20',80),
(4,'midterm','2024-03-10',40),
(4,'final','2024-05-28',60),
(5,'midterm','2023-11-12',50),
(5,'final','2023-12-21',50),
(6,'midterm','2024-03-15',40),
(6,'final','2024-05-30',60);

INSERT INTO ExamResult (exam_id,student_id,score,pass_flag) VALUES
(1,1,78,TRUE),
(1,2,65,TRUE),
(1,3,55,FALSE),
(2,1,82,TRUE),
(2,2,60,TRUE),
(3,1,70,TRUE),
(4,4,58,FALSE),
(5,6,80,TRUE),
(5,7,68,TRUE),
(6,6,73,TRUE),
(6,7,69,TRUE),
(7,8,50,FALSE),
(8,8,62,TRUE),
(9,10,90,TRUE),
(10,10,84,TRUE);
