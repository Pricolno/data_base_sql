import sqlite3
import csv

path_to_db = 'university.db'


def init_table_val(force: bool = False):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()

        if force:
            cursor.execute('DROP TABLE IF EXISTS Оценки')

        query = """ CREATE TABLE IF NOT EXISTS Оценки( 
            id INTEGER,
            предмет TEXT,
            студент TEXT,
            оценка INTEGER,
            время_получения TEXT
            )"""

        cursor.execute(query)


def init_table_subject(force: bool = False):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()

        if force:
            cursor.execute('DROP TABLE IF EXISTS Предметы')

        query = """ CREATE TABLE IF NOT EXISTS Предметы( 
            id INTEGER,
            предмет TEXT,
            преподаватель TEXT
            )"""

        cursor.execute(query)


def init_table_student(force: bool = False):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()

        if force:
            cursor.execute('DROP TABLE IF EXISTS Студенты')

        query = """ CREATE TABLE IF NOT EXISTS Студенты( 
            id INTEGER,
            имя TEXT,
            фамилия TEXT,
            страна TEXT,
            дата_рождения TEXT
            )"""

        cursor.execute(query)


def init_db(force: bool = False):
    init_table_val(force=force)
    init_table_subject(force=force)
    init_table_student(force=force)


def add_teacher_to_db(teacher_set):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()
        id = 0
        for data in teacher_set:
            id += 1
            teacher, obj = data
            db.execute(""" INSERT INTO Предметы(id, предмет, преподаватель)
            VALUES(?, ?, ?)""", (id, obj, teacher))


def add_values_to_db(value_set):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()
        id = 0
        for data in value_set:
            id += 1
            obj, name, surname, val, time = data
            student = surname + '_' + name
            db.execute(""" INSERT INTO Оценки(id, предмет, студент, оценка, время_получения)
            VALUES(?, ?, ?, ?, ?)""", (id, obj, student, val, time))


def add_student_to_db(student_set):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()
        id = 0
        for data in student_set:
            id += 1
            name, surname = data
            db.execute(""" INSERT INTO Студенты(id, имя, фамилия, страна, дата_рождения)
            VALUES(?, ?, ?, ?, ?)""", (id, name, surname, None, None))


def convert_csv_to_db():
    path_to_csv = 'exam.csv'
    with open(path_to_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        teacher_set = dict()
        student_set = dict()
        value_set = dict()
        for row in reader:
            row = ' '.join(row).split()
            val, obj, time, name, surname, teacher = row
            # запоминаем учителя-предмет
            teacher_set[teacher, obj] = 1
            # запоминаем студенты
            student_set[name, surname] = 1
            # запоминаем оценки
            value_set[obj, name, surname, val, time] = 1

        # добавляем предметы
        add_teacher_to_db(teacher_set)
        # добавляем учеников
        add_student_to_db(student_set)
        # добавляем оценки
        add_values_to_db(value_set)


def average_score_by_object(need_object):
    with sqlite3.connect(path_to_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT студент, оценка FROM Оценки WHERE предмет=?
        """, (need_object,))
        student_score = cursor.fetchall()
        student_info = dict()
        for student, score in student_score:
            surname, name = student.split('_')
            count_sum = student_info.get((surname, name))
            if count_sum is None:
                student_info[surname, name] = 1, int(score)
            else:
                student_info[surname, name] = int(count_sum[0]) + 1, int(count_sum[1]) + int(score)

        print('Средний баллы учеников по ' + need_object)
        for (surname, name) in student_info:
            count, sum = student_info[surname, name]
            print(surname, name + ': ' + str(sum / count))


if __name__ == '__main__':
    init_db(force=True)
    convert_csv_to_db()
    average_score_by_object('Математика')
