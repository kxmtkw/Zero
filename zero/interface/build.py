from zero.nodes.nodes import TargetNode
from zero.builder.builder import Builder
from .executable import Executable

class Build:
	"""
	Core class to make the build system
	"""

	def __init__(self) -> None:
		self._nodes: list[TargetNode] = []

	def add(self, exe: Executable):
		self._nodes.append(exe._make_node())
		

	def make(self):
		build = Builder()
		for n in self._nodes:
			build.visit(n)
		