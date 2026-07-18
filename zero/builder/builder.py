from zero.nodes.nodes import *
from zero.nodes.nodes import SharedLibraryNode
from zero.nodes.visitor import NodeVisitor

from zero.compilers import BaseCompiler


class Builder(NodeVisitor):

	def __init__(self, compiler: BaseCompiler) -> None:
		super().__init__()
		self.compiler = compiler
		self.compiling_shared_lib = False

		self.include_dirs: list[Path] = []


	def visitRootNode(self, node: RootNode):
		for target in node.targets:
			self.visit(target)


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		print(f">> Compiling static lib: {str(node.outfile)}")

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		
		for deps in node.sources:
			self.visit(deps)

		self.compiler.build_static_lib([n.outfile for n in node.sources], node.outfile)


	def visitSharedLibraryNode(self, node: SharedLibraryNode):

		print(f">> Compiling shared lib: {str(node.outfile)}")

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

		self.compiler.build_shared_lib([n.outfile for n in node.sources], [l.outfile for l in node.linked_libraries], node.outfile)

		self.compiling_shared_lib = False
	

	def visitExecutableNode(self, node: ExecutableNode):
		
		print(f">> Building executable: {str(node.outfile)}")

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		for deps in node.sources:
			self.visit(deps)

		self.compiler.build_executable([n.outfile for n in node.sources], [n.outfile for n in node.linked_libraries], node.outfile)

		
	def visitSourceNode(self, node: SourceNode):

		print(f"-- Building source: {node.filepath}")

		for deps in node.headers:
			self.visit(deps)

		self.compiler.build_file(node.filepath, node.outfile, for_shared=self.compiling_shared_lib, include_dirs=self.include_dirs)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.headers:
			self.visit(deps)