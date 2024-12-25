import asyncio
from core.database import db  # Предполагается, что ваш класс Database находится в файле database.py

async def create_employee_index():
    await db.create_index("employee", "id", unique=True)  # Создаём уникальный индекс на поле 'id'

# Запуск создания индекса
if __name__ == "__main__":
    asyncio.run(create_employee_index())