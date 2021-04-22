FROM amazon/aws-lambda-python:3.8

COPY app/requirements.txt requirements.txt

# Install python dependences
RUN pip install -r requirements.txt

# Copy function code
COPY app/* ./

CMD [ "app.handler" ]