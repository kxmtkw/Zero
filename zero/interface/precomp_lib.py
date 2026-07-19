from pathlib import Path

from .headers import Headers
from .source import Source
from .lib import Library


class PreCompiledLibrary(Library):
	"""
	Class to represent a pre compiled library.
	"""

	def __init__(self, filepath: str | Path) -> None:
		self.headers = Headers()
		self._filepath: Path = Path(filepath)

	@property
	def filepath(self):
		return self._filepath
	
