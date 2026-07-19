from pathlib import Path

from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import GccCompiler, GxxCompiler, ClangCompiler, ClangxxCompiler
from zero.graph.printer import NodePrinter

from zero.analysis.cycle_detector import CycleDetector


class Orchestrator:

	def __init__(self) -> None:
		pass

	def start(self, build: Build):

		print(">> Setting up build...")

		match build.compiler:
			case "gcc":
				compiler = GccCompiler()
			case "g++":
				compiler = GxxCompiler()
			case "clang":
				compiler = ClangCompiler()
			case "clang++":
				compiler = ClangxxCompiler()
			case _:
				raise RuntimeError(f"Unknown compiler specified: {build.compiler}")
			
		print(f"Chosen Compiler: {build.compiler}")

		build.directory.mkdir(511, True, True)

		build_dir = build.directory
		exec_dir = build_dir / "bin"
		object_dir = build_dir / "objects"
		lib_dir = build_dir / "lib"
		shared_dir = lib_dir / "shared"
		static_dir = lib_dir / "static"

		exec_dir.mkdir(511, True, True)
		object_dir.mkdir(511, True, True)
		shared_dir.mkdir(511, True, True)
		static_dir.mkdir(511, True, True)

		print(f"Build Directory: {build.directory}")

		print(">> Constructing build graph...")

		self.graph = GraphConstructor(
			compiler,
			build_dir,
			object_dir,
			exec_dir,
			static_dir,
			shared_dir
		)

		root = self.graph.make_root(build)

		printer = NodePrinter()
		printer.visit(root)

		print(">> Detecting cycles...")

		cycle = CycleDetector()
		cycle.visit(root)
		exit(1)
		print(">> Starting build...")

		self.builder = Builder(compiler)
		self.builder.visit(root)
