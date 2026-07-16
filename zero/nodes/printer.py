from .nodes import *
from .visitor import NodeVisitor


class NodePrinter(NodeVisitor):

	def __init__(self) -> None:
		super().__init__()
		self.depth = 0


	def visitRootNode(self, node: RootNode):
		print("-- Build Project Root --") 
		for t in node.targets:
			self.visit(t)
			print()


	def visitExecutableNode(self, node: ExecutableNode):
		print(f"Executable: {hex(id(node))}")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1


	def visitSourceNode(self, node: SourceNode):
		print("  " * self.depth,  end="")
		print(f"Source: {node.filepath} {hex(id(node))}")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1


	def visitHeaderNode(self, node: HeaderNode):
		print("  " * self.depth, end="")
		print(f"Header: {node.filepath} {hex(id(node))}")
		self.depth += 1
		for deps in node.dependencies:
			self.visit(deps)
		self.depth -= 1
