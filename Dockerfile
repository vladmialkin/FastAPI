FROM python:3.11
COPY . .
WORKDIR .
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
COPY ./app .
CMD ["uvicorn", "app.main:my_app", "--host", "0.0.0.0", "--port", "8000"]