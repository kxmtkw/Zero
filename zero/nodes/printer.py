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

		print("  " * self.depth,  end="")
		print("(Sources)\n")

		for deps in node.sources:
			self.visit(deps)

		print("  " * self.depth,  end="")
		print("(Linked Libs)\n")

		for lib in node.linked_libraries:
			print("  " * self.depth,  end="")
			print(f"Library: {hex(id(lib))}")
		
		self.depth -= 1

	
	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		print(f"Static Library: {hex(id(node))}")
		self.depth += 1

		print("  " * self.depth,  end="")
		print("(Sources)\n")

		for deps in node.sources:
			self.visit(deps)

		print("  " * self.depth,  end="")
		print("(Linked Libs)\n")

		for lib in node.linked_libraries:
			print("  " * self.depth,  end="")
			print(f"Library: {hex(id(lib))}")
		
		self.depth -= 1


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		print(f"Shared Library: {hex(id(node))}")
		self.depth += 1

		print("  " * self.depth,  end="")
		print("(Sources)\n")

		for deps in node.sources:
			self.visit(deps)

		print("  " * self.depth,  end="")
		print("(Linked Libs)\n")

		for lib in node.linked_libraries:
			print("  " * self.depth,  end="")
			print(f"Library: {hex(id(lib))}")
		
		self.depth -= 1


	def visitSourceNode(self, node: SourceNode):
		print("  " * self.depth,  end="")
		print(f"Source: {node.filepath} {hex(id(node))}")
		self.depth += 1
		for deps in node.sources:
			self.visit(deps)
		self.depth -= 1


	def visitHeaderNode(self, node: HeaderNode):
		print("  " * self.depth, end="")
		print(f"Header: {node.filepath} {hex(id(node))}")
		self.depth += 1
		for deps in node.sources:
			self.visit(deps)
		self.depth -= 1
