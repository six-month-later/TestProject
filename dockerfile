from python:3.12-slim
WORKDIR /app
COPY dependences/requirements.txt .
RUN pip install --no-cache-dir -r dependences/requirements.txt
COPY src .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]