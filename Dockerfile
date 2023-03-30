FROM ubuntu:20.04

ENV SRC_DIR /video-verticalization
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y curl ffmpeg python3 python3-pip

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH:$PATH

WORKDIR ${SRC_DIR}

# Python packages installing
COPY pyproject.toml ${SRC_DIR}
COPY poetry.lock ${SRC_DIR}
RUN poetry install --no-interaction -vvv

# Verticalization package installing separately.
# It will build quicker if you change only Verticalization code.
COPY video_verticalization/ ${SRC_DIR}/video_verticalization/
RUN poetry install --no-interaction -vvv

ENV PYTHONPATH $PYTHONPATH:${SRC_DIR}
ENV PYTHONHASHSEED 0

WORKDIR ${SRC_DIR}
ENTRYPOINT [ "poetry", "run" ]
