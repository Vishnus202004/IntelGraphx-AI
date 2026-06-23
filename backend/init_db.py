import asyncio
from app.core.database import engine, Base
from app.models.user import User
from app.models.competitor import Competitor
from app.models.alert import Alert
from app.models.prediction import Prediction
from app.models.hash import Hash

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
