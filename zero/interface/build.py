from pathlib import Path
from typing import Literal

from .lib import Library
from .executable import Executable


class Build:
	"""
	Core class to make the build system.
	"""


	def __init__(self) -> None:
		self._targets: list[Executable | Library] = []
		self._compiler: Literal["gcc", "g++", "clang", "clang++", "best"] = "best"
		self._directory: Path = Path("build")


	@property
	def compiler(self):
		"""
		Specify a compiler for the build system. 
		If not specified, finds the best matched compiler depending on the platform.
		"""
		return self._compiler


	@compiler.setter
	def compiler(self, name: Literal["gcc", "g++", "clang", "clang++", "best"]):
		self._compiler = name


	@property
	def directory(self):
		"""
		Set a directory for the build system. If not specified, defaults to ./build
		"""
		return self._directory


	@directory.setter
	def directory(self, name: str | Path):
		self._directory = Path(name)


	def add(self, target: Executable | Library):
		"""
		Add a target to the build procedure.
		 
		Some things to be cautious of:
		- This should only be used for targets that are expected as final results. \
		For example, if an executable depends on a static library but the library itself is not required as a final product, \
		then that static library should not be added.
		"""

		if isinstance(target, Executable):

			if not hasattr(target, "_source"):
				raise RuntimeError("No source specified for this executable.")
			
			self._targets.append(target)

		elif isinstance(target, Library):

			if not hasattr(target, "_source"):
				raise RuntimeError("No source specified for this library.")
			
			self._targets.append(target)