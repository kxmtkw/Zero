from pathlib import Path

from zero.errors import ZeroError
from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers import GccCompiler, GxxCompiler, ClangCompiler, ClangxxCompiler
from zero.graph.printer import NodePrinter

from zero.analyzers.cycle_detector import CycleDetector
from zero.analyzers.stale_detector import StaleDetector

from zero.interface.target import Target
from zero.orchestrator.config import BuildConfig, Directory
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
	

	def configureBuild(self, build_dir: Path, fresh_build: bool) -> BuildConfig:

		config = BuildConfig()
		config.directory = Directory()
		
		config.directory.build = build_dir
		config.directory.binary = build_dir / "bin"
		config.directory.objects = build_dir / "objects"
		config.directory.lib = build_dir / "lib"
		config.directory.shared_lib = config.directory.lib / "shared"
		config.directory.static_lib = config.directory.lib / "static"

		config.fresh_build = fresh_build

		self.reporter.taskDone("Directory", f"{str(build_dir)} chosen.")

		return config

	
	def make(self, build: Build, *, fresh: bool = False):
		
		self.reporter.startPhase("Configuration", "Configuring")
			
		config = self.configureBuild(build.directory, fresh)

		self.graph = GraphConstructor(build._compiler, config)

		root = self.graph.makeRoot(build)

		self.reporter.taskDone("Graph", "constructed")

		cycle = CycleDetector()
		cycle.visit(root)
		
		self.reporter.taskDone("Cycles", "none detected")

		if not fresh:
			stale = StaleDetector()
			stale.visit(root)
			count = stale.getStaleCount()
			msg = "no need for compilation" if count == 0 else f"detected (count = {count})"
		else:
			msg = "skipped - fresh make"
		
		self.reporter.taskDone("Staleness", msg)
		
		self.reporter.endPhase("Configuration complete.")

		self.builder = Builder(config)
		self.builder.visit(root)


	def getBuild(self, module: ModuleLoader) -> Build:
	
		build = module.getAttribute("build")

		if not isinstance(build, Build):
			raise ZeroError(f"Attribute 'build' not found or is not an instance of Build.")
		
		return build


	def getTargets(self, module: ModuleLoader) -> list[Target]:

		targets: list[Target] = []

		for name, value in module:

			if isinstance(value, Target):
				if not hasattr(value, "_name"):
					value._name = name
				targets.append(value)

		return targets


	def makeBuild(self, *, fresh: bool = False):
		module = self.loadConfigFile()
		build = self.getBuild(module)
		build._targets = self.getTargets(module)
		self.make(build, fresh=fresh)


	def makeTargets(self, target_identifiers: list[str], *, fresh: bool = False):

		module = self.loadConfigFile()
		build = self.getBuild(module)
		
		needed_targets: list[Target] = []
		targets: list[Target] = self.getTargets(module)

		for target in targets:

			if target._name in target_identifiers:
				target_identifiers.remove(target._name)
				needed_targets.append(target)


		if len(target_identifiers) > 0:
			raise ZeroError(f"Target{'s' if len(target_identifiers) > 1 else ''} not found: {', '.join(target_identifiers)}")
			
		build._targets = needed_targets

		self.make(build, fresh=fresh)


	



