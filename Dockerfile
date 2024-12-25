FROM python:3.10-slim


WORKDIR /app

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение в контейнер
COPY . .

# Запускаем индексацию перед запуском приложения
# RUN python permission/create_index.py

# Указываем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT ["sh", "-c", "PYTHONPATH=/app python /app/permission/create_index.py && uvicorn main:app --host 0.0.0.0 --port 8000"]

