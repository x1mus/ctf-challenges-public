FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV FLAG="CSC{H0pefully_Cl4ud3_d1dnt_s0lve_1t!_adb_l0gg3r?_n0_encryp710n_d113ead8b78da996}"

EXPOSE 8080/tcp

STOPSIGNAL SIGTERM

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "--timeout", "30", "app:app"]