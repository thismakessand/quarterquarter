FROM python:3.6-stretch

COPY ./requirements.txt /opt/project/
RUN pip install -r /opt/project/requirements.txt
COPY . /opt/project/

ENTRYPOINT ["python", "/opt/project/main.py"]
#CMD ["python", "/opt/project/main.py"]
