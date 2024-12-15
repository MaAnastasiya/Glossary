from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from src import models, schemas, database

# Инициализация приложения
app = FastAPI(
    title="Глоссарий",
    description="REST. FastAPI. Swagger, FastAPI и SQLite",
    version="1.0.0"
)

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=database.engine)

# Эндпоинты
@app.get("/terms/", response_model=List[schemas.Term])
def get_terms(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    terms = db.query(models.TermModel).offset(skip).limit(limit).all()
    return terms

@app.get("/terms/{term}", response_model=schemas.Term)
def get_term(term: str, db: Session = Depends(database.get_db)):
    db_term = db.query(models.TermModel).filter(models.TermModel.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return db_term

@app.post("/terms/", response_model=schemas.Term, status_code=201)
def create_term(term: schemas.TermCreate, db: Session = Depends(database.get_db)):
    db_term = db.query(models.TermModel).filter(models.TermModel.term == term.term).first()
    if db_term:
        raise HTTPException(status_code=400, detail="Термин уже существует")
    new_term = models.TermModel(term=term.term, description=term.description)
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term

@app.put("/terms/{term}", response_model=schemas.Term)
def update_term(term: str, term_update: schemas.TermUpdate, db: Session = Depends(database.get_db)):
    db_term = db.query(models.TermModel).filter(models.TermModel.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    db_term.description = term_update.description
    db.commit()
    db.refresh(db_term)
    return db_term

@app.delete("/terms/{term}")
def delete_term(term: str, db: Session = Depends(database.get_db)):
    db_term = db.query(models.TermModel).filter(models.TermModel.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    db.delete(db_term)
    db.commit()
    return {"message": "Термин успешно удален"}