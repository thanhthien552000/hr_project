from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_size=20,max_overflow=10, pool_pre_ping=True)


AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
      async with AsyncSessionLocal() as session:
         try:
            yield session
            await session.commit()
         except Exception as e:
            await session.rollback()
            raise e