import ast
from ast_decompiler import decompile


class Scrambler(ast.NodeTransformer):
	HEADER = '# This code has been scrambled using some dark magic o.O'

	def __init__(self, scramble=True):
		self.do_scramble = scramble

	def visit(self, node):
		node_out = super(Scrambler, self).visit(node)
		if hasattr(node_out, 'body') and isinstance(node_out.body, list):
			if self.do_scramble:
				node_out.body = self.scramble(node_out.body)
			else:
				node_out.body = self.unscramble(node_out.body)
		if isinstance(node_out, ast.Assign) and isinstance(node_out.value, ast.List):
			if self.do_scramble:
				node_out.value.elts = self.scramble(node_out.value.elts)
			else:
				node_out.value.elts = self.unscramble(node_out.value.elts)
		return node_out

	def scramble(self, items):
		return self._step2(self._step1(items[:]))

	def unscramble(self, items):
		return self._step1(self._step2(items[:]))

	def _step1(self, items):
		i = 0
		length = len(items)
		while (i + 1) < length:
			items[i], items[i + 1] = items[i + 1], items[i]
			i += 2
		return items

	def _step2(self, items):
		length = len(items)
		if length % 2 == 0:
			items[:length // 2], items[length // 2:] = items[length // 2:], items[:length // 2]
		else:
			items[:(length - 1) // 2], items[(length + 1) // 2:] = items[(length + 1) // 2:], items[:(length - 1) // 2]
		return items


class Magician():
	def __init__(self):
		with open("check.python", 'r') as f:
			f.readline()
			code = ''.join(f.readlines())
			root = ast.parse(code)
			self.dark = decompile(Scrambler(False).visit(root))

	def magic(self, message):
			local_namespace = {}
			exec(self.dark, globals(), local_namespace)
			check = local_namespace.get('check')
			return check(message)