from pathlib import Path

from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import Gcc
from zero.nodes.printer import NodePrinter


class Orchestrator:

	def __init__(self) -> None:
		pass

	def start(self, build: Build):

		print(">> Setting up build...")

		match build.compiler:
			case "gcc":
				compiler = Gcc()
			case _:
				raise RuntimeError(f"Unknown compiler specified: {build.compiler}")
			
		print(f"Chosen Compiler: {build.compiler}")

		build.directory.mkdir(511, True, True)
		print(f"Build Directory: {build.directory}")

		print(">> Constructing build graph...")

		self.graph = GraphConstructor(Gcc(), build.directory)
		root = self.graph.make_root(build)

		printer = NodePrinter()
		printer.visit(root)

		print(">> Starting build...")

		self.builder = Builder(Gcc())
		self.builder.visit(root)
