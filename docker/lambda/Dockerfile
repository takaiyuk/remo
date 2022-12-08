# https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html
FROM public.ecr.aws/lambda/python:3.9

ENV POETRY_HOME=/etc/poetry
ENV PATH $POETRY_HOME/bin:$PATH
ENV APP_NAME=remo

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install the function's dependencies using file requirements.txt
# generated from poetry.lock.
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code and client-secret.json
COPY ${APP_NAME} ${LAMBDA_TASK_ROOT}/${APP_NAME}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "remo.handler.lambda_handler" ]
