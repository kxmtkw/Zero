from .nodes import *
from .visitor import NodeVisitor


class NodePrinter(NodeVisitor):

	def __init__(self) -> None:
		super().__init__()
		self.depth = 0

	def visitExecutableNode(self, node: ExecutableNode):
		print(f"Executable: ")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1


	def visitSourceNode(self, node: SourceNode):
		print("  " * self.depth,  end="")
		print(f"Source: {node.filepath}")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1


	def visitHeaderNode(self, node: HeaderNode):
		print("  " * self.depth, end="")
		print(f"Header: {node.filepath}")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1
