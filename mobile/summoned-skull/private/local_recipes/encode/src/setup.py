from distutils.core import setup
from distutils.extension import Extension

extensions = [Extension('encode', ['encode.c'], language="c")]
setup(name="encode", ext_modules=extensions)