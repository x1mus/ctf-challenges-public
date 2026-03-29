from distutils.core import setup
from distutils.extension import Extension

extensions = [Extension('magic', ['magic.c'], language="c")]
setup(name="magic", ext_modules=extensions)