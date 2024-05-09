from fastapi import FastAPI
import curso_router


app = FastAPI()

app.include_router(curso_router.router,tags=['Cursos'])
app