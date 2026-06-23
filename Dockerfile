FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ORM_CRUD.py .
CMD ["uvicorn", "ORM_CRUD:app", "--host", "0.0.0.0", "--port", "8000"]
