FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh
EXPOSE 5555

ENTRYPOINT [ "./entrypoint.sh" ]
