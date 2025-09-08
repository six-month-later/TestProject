from python:3.12
COPY . .
RUN pip install -r requirenments.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]