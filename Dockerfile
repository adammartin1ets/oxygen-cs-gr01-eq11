FROM python:3.9-alpine

RUN apk update && apk upgrade --no-cache

# Install build dependencies
RUN apk add --no-cache build-base unixodbc-dev

# Install curl
RUN apk add --no-cache curl

# Download the desired package(s)
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.apk

# Install the package(s)
RUN apk add --allow-untrusted msodbcsql18_18.0.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools18_18.0.1.1-1_amd64.apk

##Download the desired package(s)
#RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.apk
#RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.apk
#
##(Optional) Verify signature, if 'gpg' is missing install it using 'apk add gnupg':
##RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.sig
##RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.sig
##
##RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import -
##RUN gpg --verify msodbcsql18_18.0.1.1-1_amd64.sig msodbcsql18_18.0.1.1-1_amd64.apk
##RUN gpg --verify mssql-tools18_18.0.1.1-1_amd64.sig mssql-tools18_18.0.1.1-1_amd64.apk
#
##Install the package(s)
#RUN apk add --allow-untrusted msodbcsql18_18.0.1.1-1_amd64.apk
#RUN apk add --allow-untrusted mssql-tools18_18.0.1.1-1_amd64.apk

ENV PYTHONBUFFERED 0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["python","-u", "src/main.py"]