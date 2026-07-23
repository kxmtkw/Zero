from pathlib import Path

from zero.interface.types import PathType


class PublicOnlyHeaders:
	"""
	List the directories to look for headers in when compiling a target. Public only.
	"""

	def __init__(self) -> None:
		self._public: list[Path] = []


	@property
	def public(self):
		return self._public
	
	@public.setter
	def public(self, dirs: tuple[PathType, ...] | PathType):
		if isinstance(dirs, (tuple)):
			self._public = [Path(d) for d in dirs]
		else:
			self._public = [Path(dirs)]


class PrivateOnlyHeaders:
	"""
	List the directories to look for headers in when compiling a target. Private only.
	"""

	def __init__(self) -> None:
		self._private: list[Path] = []

	@property
	def private(self):
		return self._private
	
	
	@private.setter
	def private(self, dirs: tuple[PathType, ...] | PathType):
		if isinstance(dirs, (tuple)):
			self._private = [Path(d) for d in dirs]
		else:
			self._private = [Path(dirs)]



class Headers(PublicOnlyHeaders, PrivateOnlyHeaders):
	"""
	List the directories to look for headers in when compiling a target.
	"""

	def __init__(self) -> None:
		super().__init__()
		self._private: list[Path] = []
		self._public: list[Path] = []