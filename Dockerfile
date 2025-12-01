FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "public.index:app", "--host", "0.0.0.0", "--reload"]
