from .nodes import *


class NodeVisitor:

	def __init__(self) -> None:
		pass


	def visit(self, node: Node):
		if isinstance(node, ExecutableNode):
			self.visitExecutableNode(node)
		elif isinstance(node, SourceNode):
			self.visitSourceNode(node)
		elif isinstance(node, HeaderNode):
			self.visitHeaderNode(node)

	
	def visitExecutableNode(self, node: ExecutableNode):
		pass

	def visitSourceNode(self, node: SourceNode):
		pass

	def visitHeaderNode(self, node: HeaderNode):
		pass
