
from zero.interface.headers import PrivateOnlyHeaders
from zero.interface.target import Target



class Executable(Target):
	"""
	Build an executable.
	"""

	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self.headers = PrivateOnlyHeaders()