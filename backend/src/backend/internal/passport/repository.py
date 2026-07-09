from backend.core import app_dependency
from backend.core.database import PassportTable


async def get_passport_by_id(passport_id: int):
    async with app_dependency.get_db_session() as session:
        passport_detail = await session.get(PassportTable, passport_id)
    return passport_detail
