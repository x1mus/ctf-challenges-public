from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour

class EncodeRecipe(IncludedFilesBehaviour, CythonRecipe):
	version = '1.0'
	name = 'encode'
	depends = [('genericndkbuild', 'sdl2'), 'setuptools']
	site_package_name = 'encode'
	url = None
	src_filename = 'src'

recipe = EncodeRecipe()