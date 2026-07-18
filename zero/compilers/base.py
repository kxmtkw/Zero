from abc import ABC, abstractmethod
from pathlib import Path


class BaseCompiler(ABC):
	"""
	Base class for Compilers utilizing pathlib.Path objects.
	"""

	def __init__(self) -> None:
		super().__init__()


	@abstractmethod
	def get_dependencies(self, filepath: Path) -> list[Path]:
		pass


	@abstractmethod
	def build_file(self, filepath: Path, outfile: Path, *, for_shared = False) -> None:  
		pass
	

	@abstractmethod
	def build_static_lib(self, objects: list[Path], outfile: Path) -> None:  
		pass


	@abstractmethod
	def build_shared_lib(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		pass


	@abstractmethod
	def build_executable(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		pass