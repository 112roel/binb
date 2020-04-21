FROM python:3.7-alpine
COPY python/. /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python write_song.py"]