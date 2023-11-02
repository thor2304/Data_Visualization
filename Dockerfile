#Using python
FROM python:3.12-slim as dev
RUN pip install --upgrade pip
# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
#Copy files to your container
COPY . ./
RUN pip install -e .
#Running your APP and doing some PORT Forwarding
EXPOSE 8070
CMD python3 src/Core/main.py

FROM dev as prod
RUN pip install gunicorn
#WORKDIR src/Core
CMD gunicorn -w 4 'Core.main:server'