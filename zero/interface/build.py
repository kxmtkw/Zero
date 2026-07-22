from pathlib import Path
from typing import Literal

from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroUserError
from zero.interface.target import Target

from zero.interface.library import Library
from zero.interface.executable import Executable


class Build:
	"""
	Core class to make the build system.
	"""


	def __init__(self) -> None:
		self._targets: list[Target] = []
		self._compiler: CompilerType = "inherit"
		self._directory: Path = Path("build")


	@property
	def compiler(self):
		"""
		Specify a compiler for the build system. 
		"""
		return self._compiler


	@compiler.setter
	def compiler(self, name: CompilerType):
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


	def add(self, target: Target, *, compiler: CompilerType = "inherit"):
		"""
		Add a target to the build procedure.
		 
		Some things to be cautious of:
		- This should only be used for targets that are expected as final results. \
		For example, if an executable depends on a static library but the library itself is not required as a final product, \
		then that static library should not be added.
		"""

		if not hasattr(target, "_source"):
			raise ZeroUserError(ValueError, "No source specified for this target.")
		
		if self._compiler is None and compiler == "inherit":
			raise ZeroUserError(
				ValueError, 
				"No compiler specified for build. Cannot inherit. Either select a compiler for the target or the build."
			)
		
		target._compiler = self._compiler if compiler == "inherit" else compiler
		self._targets.append(target)