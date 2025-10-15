FROM python:3.10
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y libgl1
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]