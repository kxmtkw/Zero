from zero.graph.nodes import *
from zero.graph.nodes import SharedLibraryNode
from zero.graph.visitor import NodeVisitor

from zero.compilers import BaseCompiler


class Builder(NodeVisitor):

	def __init__(self, compiler: BaseCompiler) -> None:
		super().__init__()
		self.compiler = compiler
		self.compiling_shared_lib = False

		self.include_dirs: list[Path] = []
		
		self.visited_nodes: set[object] = set()


	def visitRootNode(self, node: RootNode):
		for target in node.targets:
			self.visit(target)


	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		if node in self.visited_nodes:
			return

		print(f">> Compiling static lib: {str(node.libpath)}")

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		
		for deps in node.sources:
			self.visit(deps)

		self.compiler.build_static_lib([n.outpath for n in node.sources], node.libpath)
		
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

		for deps in node.sources:
			self.visit(deps)

		self.compiler.build_shared_lib([n.outpath for n in node.sources], [l.libpath for l in node.linked_libraries], node.libpath)

		self.compiling_shared_lib = False
		self.visited_nodes.add(node)
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):

		if not node.libpath.exists():
			raise RuntimeError(f"Could not find pre-compiled library: {node.libpath}")
		
		print(f">> Found Pre Compiled Lib: {str(node.libpath)}")


	def visitExecutableNode(self, node: ExecutableNode):
		if node in self.visited_nodes:
			return
		
		print(f">> Building executable: {str(node.targetpath)}")

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		for deps in node.sources:
			self.visit(deps)

		self.compiler.build_executable([n.outpath for n in node.sources], [n.libpath for n in node.linked_libraries], node.targetpath)

		self.visited_nodes.add(node)

		
	def visitSourceNode(self, node: SourceNode):
		if node in self.visited_nodes:
			return

		print(f"-- Building source: {node.filepath}")

		for deps in node.deps:
			self.visit(deps)

		self.compiler.build_file(node.filepath, node.outpath, for_shared=self.compiling_shared_lib, include_dirs=self.include_dirs)
		
		self.visited_nodes.add(node)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.deps:
			self.visit(deps)