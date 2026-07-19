from abc import ABC, abstractmethod
from .nodes import *



class NodeVisitor(ABC):


	def __init__(self) -> None:
		pass


	def visit(self, node: Node):
	
		if isinstance(node, SourceNode):
			self.visitSourceNode(node)
		elif isinstance(node, HeaderNode):
			self.visitHeaderNode(node)
		elif isinstance(node, ExecutableNode):
			self.visitExecutableNode(node)
		elif isinstance(node, StaticLibraryNode):
			self.visitStaticLibraryNode(node)
		elif isinstance(node, SharedLibraryNode):
			self.visitSharedLibraryNode(node)
		elif isinstance(node, RootNode):
			self.visitRootNode(node)


	@abstractmethod
	def visitRootNode(self, node: RootNode):
		pass 

	@abstractmethod
	def visitExecutableNode(self, node: ExecutableNode):
		pass

	@abstractmethod
	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		pass

	@abstractmethod
	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		pass
	
	@abstractmethod
	def visitSourceNode(self, node: SourceNode):
		pass

	@abstractmethod
	def visitHeaderNode(self, node: HeaderNode):
		pass
