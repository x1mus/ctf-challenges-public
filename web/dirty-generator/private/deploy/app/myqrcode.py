import qrcode
import base64
from io import BytesIO

def generate(data: str) -> str:
	qr = qrcode.make(data)
	buffer = BytesIO()
	qr.save(buffer, format="PNG")
	return base64.b64encode(buffer.getvalue()).decode()