FROM python:3.10-buster

COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

EXPOSE 8501

COPY /* ./

ENTRYPOINT ["streamlit", "run", "app.py", "--server.baseUrlPath=/dashboard/", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true"]