from zero.graph.nodes import *
from zero.graph.nodes import SharedLibraryNode
from zero.graph.visitor import NodeVisitor

from zero.compilers import BaseCompiler

from zero.reporter import getReporter


class Builder(NodeVisitor):

	def __init__(self, compiler: BaseCompiler) -> None:
		super().__init__()
		self.compiler = compiler
		self.compiling_shared_lib = False

		self.include_dirs: list[Path] = []
		self.visited_nodes: set[object] = set()
		self.current_target_arguments: list[str] = []

		self.reporter = getReporter()


	def visitRootNode(self, node: RootNode):
		self.reporter.startPhase("Compilation", "Compiling")
		for target in node.targets:
			self.visit(target)

		self.reporter.endPhase("Build complete")


	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		if node in self.visited_nodes:
			return

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		
		self.current_target_arguments = node.arguments

		for deps in node.sources:
			self.visit(deps)

		self.compiler.buildStaticLib([n.outpath for n in node.sources], node.libpath)
		
		self.reporter.taskDone("Link ", f"{node.libpath.name}")

		self.visited_nodes.add(node)


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		if node in self.visited_nodes:
			return

		print(f">> Compiling shared lib: {str(node.libpath)}")

		self.compiling_shared_lib = True

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		self.current_target_arguments = node.arguments

		for deps in node.sources:
			self.visit(deps)

		self.compiler.buildSharedLib([n.outpath for n in node.sources], [l.libpath for l in node.linked_libraries], node.libpath)
		
		self.compiling_shared_lib = False

		self.reporter.taskDone("Link ", f"{node.libpath.name}")

		self.visited_nodes.add(node)
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):

		if not node.libpath.exists():
			raise RuntimeError(f"Could not find pre-compiled library: {node.libpath}")
		
		self.reporter.taskDone("Found", f"{node.libpath}")


	def visitExecutableNode(self, node: ExecutableNode):
		if node in self.visited_nodes:
			return
		
		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		self.current_target_arguments = node.arguments

		for deps in node.sources:
			self.visit(deps)

		self.compiler.buildExecutable([n.outpath for n in node.sources], [n.libpath for n in node.linked_libraries], node.targetpath)

		self.reporter.taskDone("Link ", f"{node.targetpath.name}")

		self.visited_nodes.add(node)

		
	def visitSourceNode(self, node: SourceNode):
		if node in self.visited_nodes:
			return

		for deps in node.deps:
			self.visit(deps)

		self.compiler.buildFile(
			node.filepath, 
			node.outpath, 
			for_shared=self.compiling_shared_lib, 
			include_dirs=self.include_dirs, 
			arguments=self.current_target_arguments
		)
		
		self.reporter.taskDone("Built", f"{node.filepath}")

		self.visited_nodes.add(node)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.deps:
			self.visit(deps)