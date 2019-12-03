FROM iambillmccann/letshangbackend:parent
COPY . .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
RUN . /venv/bin/activate

EXPOSE 8000
CMD [ "gunicorn", "letshang.app" ]
