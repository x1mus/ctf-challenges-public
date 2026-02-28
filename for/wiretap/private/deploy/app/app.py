import os
from flask import Flask, request, jsonify, render_template_string, abort

app = Flask(__name__)

# ── CTF config — change these ──
VALID_USER = "x1mus"
VALID_PASS = "Please0p3nTh3D00R!!!_b6ec8bd3"
FLAG = os.environ.get("FLAG", "CSC{H0pefully_Cl4ud3_d1dnt_s0lve_1t!_adb_l0gg3r?_n0_encryp710n_d113ead8b78da996}")
# ──────────────────────────────


HTML_404 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>NexaMail — Page not found</title>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&family=Roboto:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
	*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

	body {
	  font-family: 'Roboto', sans-serif;
	  background: #f8f9fa;
	  min-height: 100vh;
	  display: flex;
	  flex-direction: column;
	  align-items: center;
	  justify-content: center;
	  color: #202124;
	  text-align: center;
	  padding: 2rem;
	}

	.logo-wordmark {
	  font-family: 'Google Sans', sans-serif;
	  font-size: 28px;
	  font-weight: 500;
	  letter-spacing: -0.5px;
	  margin-bottom: 40px;
	}

	.logo-wordmark .n  { color: #4285F4; }
	.logo-wordmark .e  { color: #EA4335; }
	.logo-wordmark .x  { color: #FBBC05; }
	.logo-wordmark .a  { color: #4285F4; }
	.logo-wordmark .m  { color: #34A853; }
	.logo-wordmark .ai { color: #EA4335; }
	.logo-wordmark .l  { color: #4285F4; }

	/* The big illustrated 404 */
	.illustration {
	  position: relative;
	  margin-bottom: 32px;
	}

	.big-number {
	  font-family: 'Google Sans', sans-serif;
	  font-size: clamp(80px, 20vw, 140px);
	  font-weight: 500;
	  line-height: 1;
	  letter-spacing: -4px;
	  color: #e8eaed;
	  user-select: none;
	}

	/* Envelope icon sitting on the 0 */
	.envelope-wrap {
	  position: absolute;
	  top: 50%;
	  left: 50%;
	  transform: translate(-50%, -54%);
	}

	.envelope {
	  width: clamp(60px, 12vw, 90px);
	  height: clamp(42px, 8.5vw, 63px);
	}

	h1 {
	  font-family: 'Google Sans', sans-serif;
	  font-size: 22px;
	  font-weight: 400;
	  color: #202124;
	  margin-bottom: 10px;
	}

	p {
	  font-size: 15px;
	  color: #5f6368;
	  max-width: 340px;
	  line-height: 1.6;
	  margin-bottom: 32px;
	}

	.btn-home {
	  display: inline-block;
	  background: #1a73e8;
	  color: #fff;
	  border: none;
	  border-radius: 4px;
	  padding: 10px 28px;
	  font-family: 'Google Sans', sans-serif;
	  font-size: 14px;
	  font-weight: 500;
	  text-decoration: none;
	  cursor: pointer;
	  transition: background 0.15s, box-shadow 0.15s;
	  letter-spacing: 0.25px;
	}

	.btn-home:hover { background: #1765cc; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }

	.page-footer { margin-top: 48px; font-size: 12px; color: #5f6368; }
  </style>
</head>
<body>

  <div class="logo-wordmark">
	<span class="n">N</span><span class="e">e</span><span class="x">x</span><span class="a">a</span><span class="m">M</span><span class="ai">ai</span><span class="l">l</span>
  </div>

  <div class="illustration">
	<div class="big-number">404</div>
	<div class="envelope-wrap">
	  <!-- Simple SVG envelope -->
	  <svg class="envelope" viewBox="0 0 90 63" fill="none" xmlns="http://www.w3.org/2000/svg">
		<!-- body -->
		<rect x="1" y="1" width="88" height="61" rx="4" fill="#fff" stroke="#dadce0" stroke-width="2"/>
		<!-- flap -->
		<path d="M1 5 L45 36 L89 5" stroke="#dadce0" stroke-width="2" fill="none"/>
		<!-- left fold -->
		<path d="M1 62 L32 33" stroke="#dadce0" stroke-width="2"/>
		<!-- right fold -->
		<path d="M89 62 L58 33" stroke="#dadce0" stroke-width="2"/>
		<!-- question mark on envelope body -->
		<text x="45" y="54" text-anchor="middle" font-family="Google Sans, sans-serif" font-size="22" fill="#9aa0a6">?</text>
	  </svg>
	</div>
  </div>

  <h1>Page not found</h1>
  <p>The page you're looking for doesn't exist or may have been moved.</p>

  <a href="javascript:history.back()" class="btn-home">Go back</a>

  <div class="page-footer">© 2025 NexaMail Inc.</div>

</body>
</html>"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<title>NexaMail — Sign in</title>
	<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&family=Roboto:wght@400;500&display=swap" rel="stylesheet"/>
	<style>
		*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

		body {
			font-family: 'Roboto', sans-serif;
			background: #f8f9fa;
			min-height: 100vh;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			color: #202124;
		}

		.card {
			background: #fff;
			border: 1px solid #dadce0;
			border-radius: 8px;
			padding: 48px 40px 36px;
			width: 100%;
			max-width: 400px;
		}

		.logo { text-align: center; margin-bottom: 16px; }

		.logo-wordmark {
			font-family: 'Google Sans', sans-serif;
			font-size: 28px;
			font-weight: 500;
			letter-spacing: -0.5px;
		}

		.logo-wordmark .n  { color: #4285F4; }
		.logo-wordmark .e  { color: #EA4335; }
		.logo-wordmark .x  { color: #FBBC05; }
		.logo-wordmark .a  { color: #4285F4; }
		.logo-wordmark .m  { color: #34A853; }
		.logo-wordmark .ai { color: #EA4335; }
		.logo-wordmark .l  { color: #4285F4; }

		h1 {
			font-family: 'Google Sans', sans-serif;
			font-size: 24px;
			font-weight: 400;
			text-align: center;
			margin-bottom: 8px;
			color: #202124;
		}

		.subtitle { font-size: 16px; color: #5f6368; text-align: center; margin-bottom: 32px; }

		.field { margin-bottom: 20px; position: relative; }

		.field input {
			width: 100%;
			padding: 13px 14px;
			border: 1px solid #dadce0;
			border-radius: 4px;
			font-size: 16px;
			font-family: 'Roboto', sans-serif;
			color: #202124;
			outline: none;
			background: transparent;
			transition: border-color 0.15s;
		}

		.field input:focus {
			border-color: #1a73e8;
			border-width: 2px;
			padding: 12px 13px;
		}

		.field label {
			position: absolute;
			left: 14px;
			top: 50%;
			transform: translateY(-50%);
			font-size: 16px;
			color: #5f6368;
			pointer-events: none;
			background: #fff;
			padding: 0 3px;
			transition: all 0.15s ease;
		}

		.field input:focus + label,
		.field input:not(:placeholder-shown) + label {
			top: 0; font-size: 12px; color: #1a73e8;
		}

		.field input:not(:focus):not(:placeholder-shown) + label { color: #5f6368; }

		.error-msg {
			font-size: 12px;
			color: #d93025;
			margin-top: 6px;
			padding-left: 14px;
			display: none;
		}

		.error-msg.show { display: block; }
		.field.has-error input { border-color: #d93025; }
		.field.has-error input:not(:focus) + label { color: #d93025; }

		.forgot {
			display: inline-block;
			font-size: 14px;
			color: #1a73e8;
			text-decoration: none;
			margin-bottom: 28px;
		}
		.forgot:hover { text-decoration: underline; }

		.actions { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }

		.create-account { font-size: 14px; color: #1a73e8; text-decoration: none; font-weight: 500; }
		.create-account:hover { text-decoration: underline; }

		.btn-signin {
			background: #1a73e8;
			color: #fff;
			border: none;
			border-radius: 4px;
			padding: 10px 24px;
			font-family: 'Google Sans', sans-serif;
			font-size: 14px;
			font-weight: 500;
			cursor: pointer;
			transition: background 0.15s, box-shadow 0.15s;
			letter-spacing: 0.25px;
		}

		.btn-signin:hover { background: #1765cc; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }

		.success-banner {
			background: #e6f4ea;
			border: 1px solid #ceead6;
			border-radius: 4px;
			padding: 14px 16px;
			margin-top: 20px;
			font-size: 14px;
			color: #137333;
			display: none;
			word-break: break-all;
		}

		.success-banner.show { display: block; }

		.server-msg {
			border-radius: 4px;
			padding: 14px 16px;
			margin-top: 20px;
			font-size: 14px;
		}

		.server-msg.success { background: #e6f4ea; border: 1px solid #ceead6; color: #137333; }
		.server-msg.error   { background: #fce8e6; border: 1px solid #f5c6c2; color: #d93025; }

		.footer { margin-top: 24px; display: flex; gap: 20px; justify-content: center; }
		.footer a { font-size: 12px; color: #5f6368; text-decoration: none; }
		.footer a:hover { text-decoration: underline; }

		.page-footer { margin-top: 20px; font-size: 12px; color: #5f6368; }
	</style>
</head>
<body>

<div class="card">
	<div class="logo">
		<div class="logo-wordmark">
			<span class="n">N</span><span class="e">e</span><span class="x">x</span><span class="a">a</span><span class="m">M</span><span class="ai">ai</span><span class="l">l</span>
		</div>
	</div>

	<h1>Sign in</h1>
	<p class="subtitle">Use your NexaMail account</p>

	{% if message %}
	<div class="server-msg {{ message_type }}">{{ message }}</div>
	{% endif %}

	<form method="POST" action="/63bb50-login" novalidate>
		<div class="field" id="fieldUser">
			<input type="text" name="username" id="username" placeholder=" " autocomplete="off" spellcheck="false"/>
			<label for="username">Email or username</label>
		</div>

		<div class="field" id="fieldPass">
			<input type="password" name="password" id="password" placeholder=" "/>
			<label for="password">Password</label>
		</div>

		<a href="#" class="forgot">Forgot password?</a>

		<div class="actions">
			<a href="#" class="create-account">Create account</a>
			<button type="submit" class="btn-signin">Next</button>
		</div>
	</form>

	<div class="footer">
		<a href="#">Privacy Policy</a>
		<a href="#">Terms of Service</a>
		<a href="#">Help</a>
	</div>
</div>

<div class="page-footer">© 2025 NexaMail Inc.</div>

</body>
</html>"""

@app.errorhandler(404)
def not_found(e):
	return render_template_string(HTML_404), 404

@app.route("/")
def index():
	abort(404)

@app.route("/63bb50-login", methods=["GET", "POST"])
def login():
	message = None
	message_type = None

	if request.method == "POST":
		username = request.form.get("username", "").strip()
		password = request.form.get("password", "")

		if username == VALID_USER and password == VALID_PASS:
			message = f"🎉 Signed in successfully! Your flag: {FLAG}"
			message_type = "success"
		else:
			message = "Wrong username/password."
			message_type = "error"

	return render_template_string(HTML, message=message, message_type=message_type)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)