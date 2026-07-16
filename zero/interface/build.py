from pathlib import Path
from typing import Literal

from zero.nodes.nodes import Node, TargetNode
from zero.builder.builder import Builder
from zero.nodes.printer import NodePrinter
from zero.graph.constructor import GraphConstructor
from zero.compilers import Gcc, Clang
from .executable import Executable


class Build:
	"""
	Core class to make the build system
	"""

	def __init__(self) -> None:
		self._targets: list[Executable] = []
		self._compiler: Literal["gcc", "clang"] | None = None
		self._directory: Path = Path("build")

	
	@property
	def compiler(self):
		return self._compiler


	@compiler.setter
	def compiler(self, name: Literal["gcc", "clang"]):
		self._compiler = name


	@property
	def directory(self):
		return self._directory


	@directory.setter
	def directory(self, name: str | Path):
		self._directory = Path(name)


	def add(self, exe: Executable):
		
		if not exe._source:
			raise RuntimeError("No source specified for this executable.")
		
		if not exe._outfile:
			raise RuntimeError("No outfile specified for this executable.")
		
		self._targets.append(exe)
		

	def make(self):

		print(">> Setting up build...")

		if self._compiler is None:
			raise RuntimeError("No compiler specified.")
		
		match self._compiler:
			case "gcc":
				compiler = Gcc()
			case "clang":
				compiler = Clang()
			case _:
				raise RuntimeError(f"Unknown compiler specified: {self._compiler}")
			
		print(f"Compiler: {self._compiler}")
		
		if not self._directory.exists():
			self._directory.mkdir()

		print(f"Build directory: {str(self._directory)}")

		graph = GraphConstructor(compiler, self._directory)
		build = Builder(compiler)

		print(">> Starting build...")
		
		for t in self._targets:
			node = graph.make_executable_node(t._outfile, t._source._sources_paths)
			build.visit(node)
		