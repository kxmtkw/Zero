from zero.nodes.nodes import TargetNode
from zero.builder.builder import Builder
from zero.nodes.printer import NodePrinter
from zero.graph.builder import GraphBuilder
from .executable import Executable

class Build:
	"""
	Core class to make the build system
	"""

	def __init__(self) -> None:
		self._targets: list[Executable] = []


	def add(self, exe: Executable):
		exe._validate_fields()
		self._targets.append(exe)
		

	def make(self):
		printer = NodePrinter()

		graph = GraphBuilder()
		build = Builder()

		for t in self._targets:
			node = graph.make_executable_node(t.outfile, t.source._sources_paths)
			printer.visit(node)
			build.visit(node)
		