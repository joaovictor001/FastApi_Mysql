from typing import List

from fastapi import APIRouter,status,Depends,HTTPException,Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schemas import CursoSchemam
from core.deps import get_session


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED,response_model=CursoSchemam)
 #O with é um gerenciador de contexto é um objeto Python que define os métodos __enter__() e __exit__(), que permitem inicializar e finalizar recursos.
async def post_curso(curso: CursoSchemam, db : AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo = curso.titulo,
                                                    aulas = curso.aulas,
                                                    horas = curso.horas,
                                                    instrutor = curso.instrutor)
    
    db.add(novo_curso)
    await db.commit()
    return novo_curso

#GET Cursos
@router.get('/', response_model=List[CursoSchemam])
async def get_cursos(db: AsyncSession = Depends(get_session)):
     #O with é um gerenciador de contexto é um objeto Python que define os métodos __enter__() e __exit__(), que permitem inicializar e finalizar recursos.
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos
    

#GET Curso
@router.get('/{cusro_id}', response_model=CursoSchemam , status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    #O with é um gerenciador de contexto é um objeto Python que define os métodos __enter__() e __exit__(), que permitem inicializar e finalizar recursos.
    async with db as  session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()

          #Caso o curso com o ID informado for encotrado, vai entrar no if 
        if curso:
            return curso
        else: 
            raise HTTPException(detail='Curso não encotrado ', status_code=status.HTTP_404_NOT_FOUND)
        
#PUT Curso
        
@router.put('/{curso_id}', response_model=CursoSchemam, status_code=status.HTTP_202_ACCEPTED)
async def put_curo(curso_id: int, curso: CursoSchemam, db: AsyncSession= Depends(get_session)):
    async with db as  session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)

        result = await session.execute(query)
        #eu atribuo o curso(result)  a varivel curso_up 
        curso_up = result.scalar_one_or_none()


        #Caso o curso com o ID informado for encotrado, vai entrar no if 
        if curso:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            curso_up.instrutor = curso.instrutor
            
            
            #Do um commit no banco para salvar a alteração dos valores
            await session.commit()
            return curso_up
        
        else: 
            raise HTTPException(detail='Curso não encotrado ', status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id:int,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()
        if curso_del:
            await session.delete(curso_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso dnão encontrado"))
        
        







