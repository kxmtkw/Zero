from zero.nodes.nodes import *
from zero.nodes.visitor import NodeVisitor

from zero.compilers import gcc

class Builder(NodeVisitor):

	def __init__(self) -> None:
		super().__init__()


	def visitExecutableNode(self, node: ExecutableNode):
		print(f">> Making Executable...")

		for deps in node.dependencies:
			self.visit(deps)

		gcc.link_exes(node.outfile, *[n.outfile for n in node.dependencies])


	def visitSourceNode(self, node: SourceNode):
		print(f"-- Building source: {node.filepath}")
		for deps in node.dependencies:
			self.visit(deps)
		gcc.build_file(node.filepath, node.outfile)
		


	def visitHeaderNode(self, node: HeaderNode):
		print(f"-- Found header: {node.filepath}")
		for deps in node.dependencies:
			self.visit(deps)