from pathlib import Path

from .static_lib import StaticLibrary
from .source import Source
from zero.nodes.nodes import ExecutableNode

class Executable:
	"""
	Class to build an executable.
	"""

	def __init__(self) -> None:
		self._source: Source
		self._outfile: Path
		self._linked_libs: list[StaticLibrary] = []


	@property
	def source(self):
		"Specify the source files for the executable. Can only be set once."	

		if not hasattr(self, "_source"):
			raise RuntimeError("Source not specified for this source.")
			
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def outfile(self):
		"Specify the output files for the executable. Can only be set once."

		if not hasattr(self, "_outfile"):
			raise RuntimeError("Outfile not specified for this source.")
		
		return self._outfile
	

	@outfile.setter
	def outfile(self, path: str | Path):
		self._outfile = Path(path)


	def link(self, library: StaticLibrary):
		"Link a library to this executable."
		self._linked_libs.append(library)
