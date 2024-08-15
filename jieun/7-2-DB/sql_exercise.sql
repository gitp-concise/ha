show databases;
use ybigta;

-- DDL
CREATE TABLE student (
    -- primary-key
    sid VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    phone_number VARCHAR(30)
);
-- DML
-- 주의: 같은 PK를 갖는 데이터를 둘 이상 넣을 수 없음
INSERT INTO student (sid, name, age, phone_number)
VALUES ('2019147500', 'Alice', 20, '123-456-7890');

CREATE TABLE assignment (
    -- auto-created primary key
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    -- foreign key
    -- many-to-one relationship
    student_sid VARCHAR(10) NOT NULL REFERENCES student(sid)
);
-- 주의: auto_increment primary key이므로 여러번 실행하면 중복되는 데이터가 들어갈 수 있음
INSERT INTO assignment (title, student_sid)
VALUES ('hello, world', '2019147500'),
    ('help me, world', '2019147500');

CREATE TABLE lecture (title VARCHAR(50) PRIMARY KEY);
-- many-to-many relationship table
CREATE TABLE student_lecture (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_sid VARCHAR(10) NOT NULL,
    lecture_title VARCHAR(50) NOT NULL,
    FOREIGN KEY (student_sid) REFERENCES student(sid),
    FOREIGN KEY (lecture_title) REFERENCES lecture(title)
);
INSERT INTO lecture (title)
VALUES ('coding'),
    ('math'),
    ('english'),
    ('database');
INSERT INTO student_lecture (student_sid, lecture_title)
VALUES ('2019147500', 'coding'),
    ('2019147500', 'english'),
    ('2019147500', 'database');
INSERT INTO student (sid, name, age, phone_number)
VALUES ('2019147501', 'Bob', 21, '123-456-7891'),
    ('2019147502', 'Charlie', 22, '123-456-7892'),
    ('2019147503', 'David', 23, '123-456-7893');
INSERT INTO student_lecture (student_sid, lecture_title)
VALUES ('2019147501', 'coding'),
    ('2019147501', 'math'),
    ('2019147502', 'english');
-- join
SELECT *
FROM student_lecture;
SELECT l.title
FROM lecture l
    JOIN student_lecture sl ON l.title = sl.lecture_title
WHERE sl.student_sid = '2019147500';