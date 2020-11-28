FROM python:3.9

# Creating Application Source Code Directory
RUN mkdir -p /k8s_pagebot/src

# Setting Home Directory for containers
WORKDIR /k8s_python_sample_code/src

# Installing python dependencies
COPY requirements.txt /k8s_pagebot/src
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /k8s_python_sample_code/src/app

# Application Environment variables
ENV APP_ENV development

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application
# TODO: run as Flask / Tornado app.
CMD ["python", "app.py"]
