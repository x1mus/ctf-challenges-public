FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y curl wget

COPY app.py .
COPY myqrcode.py .
COPY static/ static/
COPY templates/ templates/

COPY gunicorn.conf.py .

ENV FLAG="CSC{im_r34lly_1mpr3ssed!_y0u_d1d_it_dirty?!_03e97a90baf03e2c}"

EXPOSE 8080/tcp

STOPSIGNAL SIGTERM

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]