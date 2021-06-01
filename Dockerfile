FROM python:3
# ARG VCS_TAG

LABEL maintainer="Bengt Giger <bgiger@ethz.ch>"

COPY libs /app/libs
COPY app.py requirements.txt /app/
WORKDIR /app
# RUN echo $VCS_TAG >.version.txt
RUN pip install -r requirements.txt

EXPOSE 8080/tcp
RUN chown 1000 /app
RUN useradd -r -u 1000 -g users jovyan
USER jovyan:users
ENV FLASK_CONFIG=production
CMD gunicorn -b 0.0.0.0:8080 -w 4 app:app
