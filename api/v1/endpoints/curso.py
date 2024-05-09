


from typing import List

from fastapi import APIRouter,status,Depends,HTTPException,Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schemas import CursoSchemam
from core.deps import get_session


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED,response_model=CursoSchemam)
async def post_curso(curso:CursoSchemam, db : AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo = curso.titulo,
                                                    aulas = curso.aulas,
                                                    horas = curso.horas,
                                                    instrutor = curso.instrutor)
    
    db.add(novo_curso)
    await db.commit()
    return novo_curso