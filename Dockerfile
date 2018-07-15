FROM debian:stable-slim

COPY requirements.txt  /usr/src/riegspy-soap/

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
    && pip install -r /usr/src/riegspy-soap/requirements.txt \
    && rm -rf /root/.cache \
    && apt-get purge -y --auto-remove build-essential

RUN wget https://github.com/Zenchreal/ZSI/archive/master.zip -O /usr/src/ZSI.zip \
    && unzip /usr/src/ZSI.zip -d /usr/src/ \
    && cd /usr/src/ZSI-master \
    && python setup.py build \
    && python setup.py install

COPY . /usr/src/riegspy-soap/

RUN python -m compileall /usr/src/riegspy-soap/ \
    && cd /usr/src/riegspy-soap/ \
    && chmod a+rx ./server.py \
    && useradd -ms /bin/bash soap_server

USER soap_server
WORKDIR /usr/src/riegspy-soap/
EXPOSE 8080
CMD [ "python", "server.py", "8080" ]
