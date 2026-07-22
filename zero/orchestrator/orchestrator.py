from pathlib import Path

from zero.errors import ZeroError
from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import GccCompiler, GxxCompiler, ClangCompiler, ClangxxCompiler
from zero.graph.printer import NodePrinter

from zero.analyzers.cycle_detector import CycleDetector

from zero.reporter import TerminalReporter

from zero.utils import ModuleLoader


class Orchestrator:

	def __init__(self) -> None:
		self.reporter = TerminalReporter()
		self.config_file = Path("zero.py")


	def loadConfigFile(self) -> ModuleLoader:

		if not self.config_file.exists():
			raise ZeroError(f"Config file '{str(self.config_file)}' not found.")
		
		try:
			module = ModuleLoader(self.config_file)
		except Exception as e:
			raise ZeroError(f"[{e.__class__.__name__}] {str(e)}")
		
		return module
	

	def makeBuild(self):

		module = self.loadConfigFile()

		build = module.getAttribute("build")

		if not isinstance(build, Build):
			raise ZeroError(f"Attribute 'build' not found or is not an instance of Build")

		self.reporter.startPhase("Configuration", "Configuring")
			
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
			build._compiler,
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


		self.builder = Builder()
		self.builder.visit(root)


	



