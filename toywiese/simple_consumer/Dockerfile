# Simple Producer

FROM continuumio/miniconda

LABEL name="Simple Listener"

USER $CONTAINER_USER

COPY requirements.txt .

# Install Python packages
RUN pip install -r 'requirements.txt' \
    && conda clean -yt

WORKDIR /home/$CONTAINER_USER

COPY *.py ./
COPY run.sh ./

CMD ["bash", "run.sh"]
