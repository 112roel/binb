FROM python:3.7-alpine
COPY python/requirements.txt /app
COPY python/write_song.py /app
COPY python/test.yml /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python write_song.py"]