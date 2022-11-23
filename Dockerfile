FROM python:3.10-buster

ARG UNAME=appuser
ARG UID=1000
ARG GID=1000

COPY / ./app/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /app/requirements.txt

EXPOSE 8501

RUN bash -c 'if [[ ${ostype} == Linux ]] ; then addgroup --gid ${GID} ${UNAME} && \
    adduser --uid ${UID} --gid ${GID} --disabled-password --gecos "" ${UNAME} && \
    chown -R ${UID}:${GID} /app ; fi'
USER ${UNAME}

WORKDIR /app

CMD ["streamlit", "run", "app.py", "--server.baseUrlPath=/dashboard/", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true"]