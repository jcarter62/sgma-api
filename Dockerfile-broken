from python:3.10

#
# define the image name to sgma-api
LABEL name="sgma-api"
# define the maintainer of the image
LABEL maintainer="Jim Carter"
LABEL version="1.0"
LABEL description="This is the Dockerfile for the sgma-api"
#

RUN apt-get update
# RUN apt-get install wget -y
#
# install odbc driver for sql server
#WORKDIR /tmp
#RUN wget https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -
#RUN wget https://packages.microsoft.com/config/ubuntu/20.04/prod.list
#RUN mv prod.list /etc/apt/sources.list.d/mssql-release.list
#RUN apt-get update
#RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
#RUN apt-get install mssql-tools -y
#RUN apt-get install unixodbc-dev -y
#RUN apt-get install libgssapi-krb5-2 -y
#RUN apt-get install libaio1 -y
#RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
#RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
#RUN source ~/.bashrc
#
#
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Los_Angeles apt-get install -y tzdata
#
RUN apt-get install sudo -y && apt-get install git -y && apt-get install nano -y && apt-get install curl -y
# RUN apt-get install python3.10 -y && apt-get install python3-pip -y && apt-get install python3-venv -y
RUN pip install "uvicorn[standard]"
#
# install pyodbc and dependencies for sql server
RUN apt-get install unixodbc-dev -sy
#
RUN mkdir /app
WORKDIR /app
#
RUN git clone https://github.com/jcarter62/sgma-api.git /app && cd /app && chmod +x start-api.sh
COPY ./.env /app/.env
# RUN python3 -m venv venv && . venv/bin/activate
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
#
EXPOSE 5150
#
CMD ["./start-api.sh"]
