from zero.nodes.nodes import *
from zero.nodes.nodes import SharedLibraryNode
from zero.nodes.visitor import NodeVisitor

from zero.compilers import BaseCompiler


class Builder(NodeVisitor):

	def __init__(self, compiler: BaseCompiler) -> None:
		super().__init__()
		self.compiler = compiler


	def visitRootNode(self, node: RootNode):
		for target in node.targets:
			self.visit(target)


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		for deps in node.sources:
			self.visit(deps)

		for libs in node.linked_libraries:
			self.visit(libs)
			
		self.compiler.build_static_lib([n.outfile for n in node.sources], node.outfile)

		print(f">> Linked static library: {str(node.outfile)}")


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		return super().visitSharedLibraryNode(node)
	

	def visitExecutableNode(self, node: ExecutableNode):

		for deps in node.sources:
			self.visit(deps)

		for libs in node.linked_libraries:
			self.visit(libs)

		self.compiler.build_executable([n.outfile for n in node.sources], [n.outfile for n in node.linked_libraries], node.outfile)

		print(f">> Linked executable: {str(node.outfile)}")


	def visitSourceNode(self, node: SourceNode):

		print(f"-- Building source: {node.filepath}")

		for deps in node.headers:
			self.visit(deps)

		self.compiler.build_file(node.filepath, node.outfile)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.headers:
			self.visit(deps)