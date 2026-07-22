from zero.interface.target import Target
from zero.interface.library import Library
from zero.interface.headers import Headers

class SharedLibrary(Target, Library):
	"""
	Class to build a shared library
	"""

	def __init__(self) -> None:
		super().__init__()
		self.headers = Headers()