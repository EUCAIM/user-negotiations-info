FROM python:3.12.7-slim

WORKDIR /opt/user-negotiations-info

COPY src/ /opt/user-negotiations-info/
COPY requirements.txt /opt/user-negotiations-info

ENV VIRTUAL_ENV=/opt/.env

RUN useradd -m flask \
    && python -m venv $VIRTUAL_ENV \
    && . /opt/.env/bin/activate \
    && pip3 install -r /opt/user-negotiations-info/requirements.txt \
    && cp /opt/user-negotiations-info/config_example.json /opt/user-negotiations-info/config.json  \
    && chown flask:flask -R /opt/user-negotiations-info \
    && chown flask:flask -R /opt/.env 

EXPOSE 8080

USER flask
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV USER_NEGOTIATIONS_INFO_CONFIG="/opt/user-negotiations-info/config.json"

CMD ["flask", "run", "--host=0.0.0.0", "-p", "8080"]