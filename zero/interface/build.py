from pathlib import Path
from typing import Literal


from .executable import Executable
from .static_lib import StaticLibrary


class Build:
	"""
	Core class to make the build system. 
	"""

	def __init__(self) -> None:
		self._targets: list[Executable | StaticLibrary] = []

		self._compiler: Literal["gcc", "clang"] | None = None
		self._directory: Path | None = None

	
	@property
	def compiler(self):
		"Specify a compiler."
		return self._compiler


	@compiler.setter
	def compiler(self, name: Literal["gcc", "clang"]):
		self._compiler = name


	@property
	def directory(self):
		return self._directory


	@directory.setter
	def directory(self, name: str | Path):
		self._directory = Path(name)


	def add(self, target: Executable | StaticLibrary):
		
		if isinstance(target, Executable):

			if not target._source:
				raise RuntimeError("No source specified for this executable.")
			
			if not target._outfile:
				raise RuntimeError("No outfile specified for this executable.")
			
			self._targets.append(target)

		elif isinstance(target, StaticLibrary):

			if not target._source:
				raise RuntimeError("No source specified for this library.")
			
			if not target._outfile:
				raise RuntimeError("No outfile specified for this library.")
			
			self._targets.append(target)