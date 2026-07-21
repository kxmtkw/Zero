import sys
import traceback

class ZeroError(Exception):
	"""
	Base class for all zero related errors.
	"""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
			

class ZeroUserError(ZeroError):
	"""
	Class for user errors related to the Zero Api. For example, source file not found or unknown compiler.
	"""

	def __init__(self, exce: type[Exception], *args: object) -> None:
		super().__init__(*args)
		self.exce = exce
