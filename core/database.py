from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import Settings


engine: AsyncEngine = create_async_engine(Settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit= False,
    autoFlush= False,
    expire_on_comit=False,
    class_=AsyncSession,
    bind=engine
)