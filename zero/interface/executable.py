from pathlib import Path

from zero.interface.lib import Library

from .static_lib import StaticLibrary
from .source import Source
from zero.nodes.nodes import ExecutableNode


class Executable:
	"""
	Class to build an executable.
	"""

	def __init__(self, name: str) -> None:
		self._source: Source
		self._name: str = name
		self._linked_libs: list[Library] = []


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
	def name(self):
		"Specify the output files for the executable. Can only be set once."

		if not hasattr(self, "_name"):
			raise RuntimeError("name not specified for this source.")
		
		return self._name
	

	def link(self, library: Library):
		"Link a library to this executable."
		self._linked_libs.append(library)
