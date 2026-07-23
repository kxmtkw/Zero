import importlib.util
from pathlib import Path


class ModuleLoader:
	"""
	Load a python file as a module.
	"""

	def __init__(self, file_path: Path):

		if not file_path.is_file():
			raise FileNotFoundError(f"File not found: {file_path}")
		
		module_name = file_path.stem

		spec = importlib.util.spec_from_file_location(module_name, file_path)
		if spec is None or spec.loader is None:
			raise ImportError(f"Cannot load module from {file_path}")
		
		self.module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(self.module)


	def getAttribute(self, name: str, default = None):
		return getattr(self.module, name, default)


	def hasAttribute(self, name: str):
		return hasattr(self.module, name)
	
	
	def __iter__(self):
		for key in dir(self.module):
			if not key.startswith("_"):
				yield key, getattr(self.module, key)