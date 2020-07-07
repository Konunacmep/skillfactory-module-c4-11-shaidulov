from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///todoslist.sqlite')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    is_completed = Column(Boolean)
    
    def __repr__(self):
        return f'{{"description":"{self.description}", "is_completed":{1 if self.is_completed else 0}}}'

Base.metadata.create_all(engine)
# добавление новой записи
def addNewEntry(descr, is_compl):
    newTodo = Todos(description=descr, is_completed=is_compl)
    session.add(newTodo)
    session.commit()
    return 'добавлена'
# получение всех записей
def getAllEntries():
    return session.query(Todos).all().__repr__()
# обновление записи
def updateEntry(descr_old, is_compl_old, descr, is_compl):
    query = session.query(Todos).filter_by(description=descr_old, is_completed=is_compl_old).first()
    if query:
        query.description = descr
        query.is_completed = True if is_compl else False
        session.commit()
        return 'изменена'
    else: return 'отсутствует в БД'
# удаление записи   
def deleteEntry(descr, is_compl):
    query = session.query(Todos).filter_by(description=descr, is_completed=is_compl).first()
    if query:
        session.delete(query)
        session.commit()
        return 'удалена'
    else: return 'отсутствует в БД'