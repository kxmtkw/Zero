
from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroUserError
from zero.interface.source import Source
from zero.interface.library import Library

from zero.compilers.base import BaseCompiler


class Target:
	"""
	Base class to represent a target.
	Should not be created manually.
	"""

	def __init__(self, **kwargs,) -> None:
		self._linked_libs: list[Library] = []
		self._arguments: list[str] = []
		
		self._name: str
		self._source: Source
		self._compiler: CompilerType = "inherit"


	@property
	def linkedLibs(self):
		"Libraries linked against this target."
		return self._linked_libs
	

	@property
	def source(self):
		"Specify the source files for the executable. Can only be set once."	

		if not hasattr(self, "_source"):
			raise ZeroUserError(ValueError, "Source not specified for this target.")
			
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def arguments(self):
		return self._arguments
	
	
	@arguments.setter
	def arguments(self, args: tuple[str, ...] | str):
		if isinstance(args, (tuple)):
			self._arguments = [arg for arg in args]
		else:
			self._arguments = [args]


	def link(self, library: Library):
		"Link a library to this target."
		self._linked_libs.append(library)
