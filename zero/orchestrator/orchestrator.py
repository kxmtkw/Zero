from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import Gcc


class Orchestrator:

	def __init__(self) -> None:
		pass

	def make(self, build: Build):

		self.graph = GraphConstructor(Gcc(), build.directory)
		self.builder = Builder(Gcc())

		root = self.graph.make_root(build)

		self.builder.visit(root)
