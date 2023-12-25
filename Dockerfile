FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN apk add --no-cache gcc musl-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade azure-cli

COPY . /app/
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]