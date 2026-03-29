import os, hashlib
from flask import Flask, request, render_template, Response
import myqrcode

app = Flask(__name__)

# ── CTF config — change these ──
FLAG = os.environ.get("FLAG", "CSC{im_r34lly_1mpr3ssed!_y0u_d1d_it_dirty?!_03e97a90baf03e2c}")
with open("flag.txt", "w") as f:
	f.write(FLAG)
# ──────────────────────────────

def valid_filename(filename):
	parts = filename.split(".")
	if len(parts) > 2:
		return False
	return all(part.isalpha() for part in parts)

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: flag.txt\n", mimetype="text/plain")

@app.route("/", methods=["GET", "POST"])
def index():
	qr_b64 = None
	error = None
	if request.method == "POST":
		file = request.files.get("file")
		if not file or file.filename == "":
			error = "No file selected."
		elif file.filename == "flag.txt":
			error = "You cannot overwrite flag.txt."
		elif file.filename == "app.py":
			error = "You cannot overwrite app.py."
		elif file.filename == "myqrcode.py":
			error = "You cannot overwrite myqrcode.py."
		elif file.filename.endswith(".py") or file.filename.endswith(".pyc"):
			error = "You cannot upload python files"
		elif not valid_filename(file.filename):
			error = "Only alphabetic characters and at most one dot are allowed."
		else:
			content = file.read()
			sha = hashlib.sha256(content).hexdigest()
			file.seek(0)
			file.save(file.filename)
			qr_b64 = myqrcode.generate(f"The SHA256 checksum of your file is: {sha}")
	return render_template("index.html", qr=qr_b64, error=error)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)