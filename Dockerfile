FROM python:3.11
COPY . .
WORKDIR .
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD [ "alembic", "revision", "--autogenerate", ";", "alembic", "upgrade", "head"]
WORKDIR /app
CMD ["uvicorn", "main:my_app", "--host", "0.0.0.0"]