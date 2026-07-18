from pathlib import Path
from .source import Source

class StaticLibrary:
	"""
	Class to build a static library.
	"""

	def __init__(self) -> None:
		self._source: Source
		self._outfile: Path
		self._linked_libs: list[StaticLibrary] = []


	@property
	def source(self):

		if not hasattr(self, "_source"):
			raise RuntimeError("Source not specified for this library.")
		
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def outfile(self):

		if not hasattr(self, "_outfile"):
			raise RuntimeError("Outfile not specified for this library.")
		
		return self._outfile
	

	@outfile.setter
	def outfile(self, path: str | Path):
		self._outfile = Path(path)


	def link(self, library: StaticLibrary):
		self._linked_libs.append(library)