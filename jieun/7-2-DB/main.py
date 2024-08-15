from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from crud import get_all_students, insert_student, delete_student
from models import Student

def main():
    db = SessionLocal()

    print("student 테이블 전체 조회")
    students = get_all_students(db)
    for student in students:
        print(f"sid: {student.sid}, name: {student.name}, age: {student.age}, phone_number: {student.phone_number}")

    print("\nstudent 테이블에 데이터 삽입")
    insert_student(db, "2021122070", "Hailey", 23, "123-456-7890")

    print("\n데이터 삽입 후 student 테이블 전체 조회")
    students = get_all_students(db)
    for student in students:
        print(f"sid: {student.sid}, name: {student.name}, age: {student.age}, phone_number: {student.phone_number}")

if __name__ == "__main__":
    main()