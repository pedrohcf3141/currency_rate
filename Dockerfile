FROM python:3.10-slim-buster

ARG ENVIRONMENT
ARG USER_ID=1001

ENV USERNAME currency_rate

ENV WORK_DIR /opt/currency_rate/src/
ENV ENVIRONMENT $ENVIRONMENT
ENV REQUIREMENTS_DIR /opt/currency_rate/requirements
ENV CMD_DIR /opt/currency_rate/commands
ENV PATH=${PATH}:/home/${USERNAME}/.local/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $WORK_DIR

RUN mkdir -p $REQUIREMENTS_DIR && mkdir -p $CMD_DIR

RUN groupadd --gid $USER_ID $USERNAME && \
    useradd --uid $USER_ID --gid $USER_ID -m $USERNAME

COPY ./src/ $WORK_DIR
COPY ./requirements/${ENVIRONMENT}.txt ${REQUIREMENTS_DIR}/${ENVIRONMENT}.txt
COPY ./commands/${ENVIRONMENT}.sh ${CMD_DIR}/${ENVIRONMENT}.sh

RUN chown -R $USERNAME /opt/ && \
    chgrp -R $USERNAME /opt/

USER $USERNAME

RUN pip install --user -r ${REQUIREMENTS_DIR}/${ENVIRONMENT}.txt

RUN chmod u+x ${CMD_DIR}/${ENVIRONMENT}.sh

CMD ["sh", "-c", "bash ${CMD_DIR}/${ENVIRONMENT}.sh"]
