FROM python:alpine3.7
COPY . /coda-test
WORKDIR /coda-test
RUN python3 -m virtualenv coda-env
RUN source coda-env/bin/activate
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "regulate_ec2.py" ]
