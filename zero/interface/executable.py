from pathlib import Path

from .source import Source
from zero.nodes.nodes import ExecutableNode

class Executable:
	"""
	Class to build an executable.
	"""

	def __init__(self) -> None:
		self._source: Source | None = None
		self._outfile: Path | None = None
		self._exe_node: ExecutableNode | None = None


	@property
	def source(self):
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def outfile(self):
		return self._outfile
	

	@outfile.setter
	def outfile(self, path: str | Path):
		self._outfile = Path(path)


	def _str(self, depth=1):
		indent = "  " * depth
		src = f"{indent}{self._source._str(depth+1)}" if self._source else f"{indent}Source: None"
		return f"Executable:\n{src}"
	

	def __str__(self) -> str:
		return self._str()