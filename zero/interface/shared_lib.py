from pathlib import Path

from .headers import Headers
from .source import Source
from .lib import Library


class SharedLibrary(Library):
	"""
	Class to build a shared library.
	"""

	def __init__(self, name: str) -> None:
		self.headers = Headers()
		self._source: Source
		self._name: str = name
		self._linked_libs: list[Library] = []


	@property
	def source(self):

		if not hasattr(self, "_source"):
			raise RuntimeError("Source not specified for this library.")
		
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def name(self):

		if not hasattr(self, "_name"):
			raise RuntimeError("Outfile not specified for this library.")
		
		return self._name
	

	@name.setter
	def name(self, name: str):
		self._name = name


	def link(self, library: Library):
		self._linked_libs.append(library)