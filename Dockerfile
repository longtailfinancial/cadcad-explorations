# A docker file to containerized the environment for 3.10 
# for the LTF team.
#
# Author: Nicholas O'Kelley
#
# Date: March 25, 2022
#
FROM python:3.10-slim-buster

ARG NB_USER=longtailer
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}


RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

WORKDIR ${HOME}

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "-m" ]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
