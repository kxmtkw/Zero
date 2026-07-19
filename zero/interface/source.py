from pathlib import Path
from zero.graph.nodes import SourceNode

class Source:
	"""
	Specify source files for a target.
	"""

	def __init__(self, *files: str | Path) -> None:

		self._sources_paths: list[Path] = []

		for f in files:
			p = Path(f)

			if not p.exists():
				raise RuntimeError(f"Source file not found: {str(p)}")
			
			self._sources_paths.append(p)
