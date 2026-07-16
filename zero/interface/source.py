from pathlib import Path
from zero.nodes.nodes import SourceNode

class Source:
	"""
	Specify source files for a target.

	Files are resolved into absolute paths with duplicate files removed.
	"""

	def __init__(self, *files: str) -> None:

		self._sources: list[str] = list(dict.fromkeys(files))
		self._sources_paths: list[Path] = []

		for s in self._sources:
			p = Path(s)

			if not p.exists():
				raise RuntimeError(f"Source file not found: {p}")
			
			self._sources_paths.append(p)



	def _str(self, depth=1) -> str:
		indent = "  " * depth
		return f"Source:\n{'\n'.join([f'{indent}{s}' for s in self._sources])}"
	

	def __str__(self) -> str:
		return self._str()
