from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

MAX_SUMMARY_LENGTH = 119


class BadSummaryError(Exception):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    summary = Column(String)
    description = Column(String)


def validate_summary(summary):
    if len(summary) > MAX_SUMMARY_LENGTH or "\n" in summary:
        raise BadSummaryError


class TaskStore:
    def __init__(self, engine_spec):
        # in memory database
        self.engine = create_engine(engine_spec)
        Base.metadata.create_all(self.engine)  # create table if not exist
        self.Session = sessionmaker(bind=self.engine)

    def get_all_tasks(self):
        return [
            {"id": task.id, "summary": task.summary}
            for task in self.Session().query(Task).all()
        ]

    def create_tasks(self, summary, description):
        validate_summary(summary)
        session = self.Session()
        task = Task(
            summary=summary,
            description=description
        )
        session.add(task)  # register the obj
        session.commit()
        return task.id

    def task_details(self, task_id):
        task = self.Session().query(Task).get(task_id)
        if task is None:
            return None
        return {
            "id": task.id,
            "summary": task.summary,
            "description": task.description
        }

    def delete_all_tasks(self):
        session = self.Session()
        session.query(Task).delete()
        session.commit()

    def delete_task(self, task_id):
        session = self.Session()
        task = session.query(Task).get(task_id)
        if task is None:
            deleted = False
        else:
            deleted = True
            session.delete(task)
            session.commit()
        return deleted

    def modify_task(self, task_id, summary, description):
        validate_summary(summary)
        session = self.Session()
        task = session.query(Task).get(task_id)
        if task is None:
            modified = False
        else:
            modified = True
            task.summary = summary
            task.description = description
            session.add(task)
            session.commit()
        return modified
