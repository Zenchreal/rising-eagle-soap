FROM debian:stable-slim

COPY requirements.txt  /usr/src/rising-eagle-soap/

RUN apt_packages=" \
        build-essential \
        python2.7 \
        python2.7-dev \
        python-pip \
        unzip \
        wget \
    "; \
    apt-get update && apt-get install -y --no-install-recommends $apt_packages && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade setuptools wheel \
    && pip install -r /usr/src/rising-eagle-soap/requirements.txt \
    && rm -rf /root/.cache \
    && apt-get purge -y --auto-remove build-essential

RUN wget https://github.com/Zenchreal/ZSI/archive/master.zip -O /usr/src/ZSI.zip \
    && unzip /usr/src/ZSI.zip -d /usr/src/ \
    && cd /usr/src/ZSI-master \
    && python setup.py build \
    && python setup.py install

COPY server.py /usr/src/rising-eagle-soap/
COPY soap/ /usr/src/rising-eagle-soap/soap/

RUN python -m compileall /usr/src/rising-eagle-soap/ \
    && cd /usr/src/rising-eagle-soap/ \
    && chmod a+rx ./server.py \
    && useradd -ms /bin/bash soap_server

USER soap_server
WORKDIR /usr/src/rising-eagle-soap/
EXPOSE 8080
CMD [ "python", "server.py", "8080" ]
