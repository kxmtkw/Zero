from pathlib import Path


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
	def public(self, *dirs: str | Path):
		self._public.clear()
		for d in dirs:
			if isinstance(d, str):
				self._public.append(Path(d))
				continue
			self._public.append(d)



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
	def private(self, *dirs: str | Path):
		self._private.clear()
		for d in dirs:
			if isinstance(d, str):
				self._private.append(Path(d))
				continue
			self._private.append(d)



class Headers(PublicOnlyHeaders, PrivateOnlyHeaders):
	"""
	List the directories to look for headers in when compiling a target.
	"""

	def __init__(self) -> None:
		super().__init__()
		self._private: list[Path] = []
		self._public: list[Path] = []