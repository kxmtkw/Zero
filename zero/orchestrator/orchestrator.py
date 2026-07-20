from pathlib import Path

from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import GccCompiler, GxxCompiler, ClangCompiler, ClangxxCompiler
from zero.graph.printer import NodePrinter

from zero.analyzers.cycle_detector import CycleDetector

from zero.reporter import TerminalReporter


class Orchestrator:

	def __init__(self) -> None:
		self.reporter = TerminalReporter()


	def start(self, build: Build):

		self.reporter.startPhase("Configuration", "Configuring")

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
			
		self.reporter.taskDone("Compiler", f"{build.compiler} chosen.")

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

		self.reporter.taskDone("Directory", f"{str(build_dir)} chosen.")


		self.graph = GraphConstructor(
			compiler,
			build_dir,
			object_dir,
			exec_dir,
			static_dir,
			shared_dir
		)

		root = self.graph.makeRoot(build)

		cycle = CycleDetector()
		cycle.visit(root)

		self.reporter.taskDone("Graph", "constructed (no cycles).")

		self.reporter.endPhase("Configuration complete.")


		self.builder = Builder(compiler)
		self.builder.visit(root)

