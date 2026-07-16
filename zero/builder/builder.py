from zero.nodes.nodes import *
from zero.nodes.visitor import NodeVisitor

from zero.compilers import BaseCompiler


class Builder(NodeVisitor):

	def __init__(self, compiler: BaseCompiler) -> None:
		super().__init__()
		self.compiler = compiler


	def visitExecutableNode(self, node: ExecutableNode):
		print(f">> Making Executable...")

		for deps in node.dependencies:
			self.visit(deps)

		self.compiler.link([n.outfile for n in node.dependencies], node.outfile)


	def visitSourceNode(self, node: SourceNode):
		print(f"-- Building source: {node.filepath}")
		for deps in node.dependencies:
			self.visit(deps)

		self.compiler.build_file(node.filepath, node.outfile)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.dependencies:
			self.visit(deps)