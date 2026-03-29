from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour

class MagicRecipe(IncludedFilesBehaviour, CythonRecipe):
	version = '1.0'
	name = 'magic'
	depends = [('genericndkbuild', 'sdl2'), 'setuptools']
	site_package_name = 'magic'
	url = None
	src_filename = 'src'

recipe = MagicRecipe()