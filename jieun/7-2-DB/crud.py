from sqlalchemy.orm import Session
from models import Student

def get_all_students(db: Session) -> list[Student]:
    return db.query(Student).all()

def insert_student(db: Session, sid: str, name: str, age: int, phone_number: str) -> Student:
    new_student = Student(sid=sid, name=name, age=age, phone_number=phone_number)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def delete_student(db: Session, sid: str) -> None:
    student = db.query(Student).filter(Student.sid == sid).first()
    if student:
        db.delete(student)
        db.commit()
        print(f"학번이 {sid}인 학생이 삭제되었습니다.")
    else:
        print(f"학번이 {sid}인 학생이 존재하지 않습니다.")