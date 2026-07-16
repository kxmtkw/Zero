from zero.nodes.nodes import *
from zero.nodes.visitor import NodeVisitor

from zero.compilers.gcc import Compiler

class Builder(NodeVisitor):

	def __init__(self) -> None:
		super().__init__()


	def visitExecutableNode(self, node: ExecutableNode):
		print(f">> Making Executable...")

		for deps in node.dependencies:
			self.visit(deps)

		Compiler().link(node.outfile, *[n.outfile for n in node.dependencies])


	def visitSourceNode(self, node: SourceNode):
		print(f"-- Building source: {node.filepath}")
		for deps in node.dependencies:
			self.visit(deps)

		node.outfile = node.filepath.parent / (node.filepath.name + ".o")
		Compiler().build_file(node.filepath, node.outfile)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.dependencies:
			self.visit(deps)