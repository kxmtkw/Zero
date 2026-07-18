from abc import abstractmethod


class Library:
	
	"""
	Base class to denote a library. Purely exists for type hints lol.
	"""

	@abstractmethod
	def __init__(self) -> None:
		pass