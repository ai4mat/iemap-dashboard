FROM python:3.9.1-slim-buster

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requiremts.txt

EXPOSE 8501

COPY ./app

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]