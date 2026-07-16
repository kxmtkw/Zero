from zero.nodes.nodes import Node, TargetNode
from zero.builder.builder import Builder
from zero.nodes.printer import NodePrinter
from zero.graph.constructor import GraphConstructor
from .executable import Executable

class Build:
	"""
	Core class to make the build system
	"""

	def __init__(self) -> None:
		self._targets: list[TargetNode] = []


	def add(self, exe: Executable):
		
		graph = GraphConstructor()

		if not exe._source:
			raise RuntimeError("No source specified for this executable.")
		
		if not exe._outfile:
			raise RuntimeError("No outfile specified for this executable.")
		
		node = graph.make_executable_node(exe._outfile, exe._source._sources_paths)

		self._targets.append(node)
		

	def make(self):
		printer = NodePrinter()
		build = Builder()

		for t in self._targets:
			printer.visit(t)
			build.visit(t)
		