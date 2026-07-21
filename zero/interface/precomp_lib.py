from pathlib import Path

from .headers import PublicOnlyHeaders
from .source import Source
from .library import Library


class PreCompiledLibrary(Library):
	"""
	Class to represent a pre compiled library.
	"""

	def __init__(self, filepath: str | Path) -> None:
		super().__init__()
		self.headers = PublicOnlyHeaders()
		self._filepath = Path(filepath)


	@property
	def filepath(self):
		return self._filepath