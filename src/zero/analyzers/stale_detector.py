from zero.graph.nodes import Node
from zero.graph.visitor import NodeVisitor
from zero.graph.nodes import *

from zero.reporter import getReporter


def markStale(node: Node):
	setattr(node, "_stale", True)


def isStale(node: Node) -> bool:
	return hasattr(node, "_stale")


class StaleDetector(NodeVisitor):


	def __init__(self) -> None:
		self.visited_nodes: set[Node] = set()
		self.current_source_outpath: Path | None = None	
		self.stale_count = 0


	def markStale(self, node: Node):
		if not hasattr(node, "_stale"):
			setattr(node, "_stale", True)
			self.stale_count += 1


	def getStaleCount(self) -> int:
		return self.stale_count
		

	def visitRootNode(self, node: RootNode):

		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return
		
	
		for t in node.targets:
			self.visit(t)


		
	def visitExecutableNode(self, node: ExecutableNode):

		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return
		

		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return

		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return


		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):
		
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return



	def visitSourceNode(self, node: SourceNode):
		
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return


		if not node.outpath.exists():
			self.markStale(node)
			return
		
		if node.outpath.stat().st_mtime < node.filepath.stat().st_mtime:
			self.markStale(node)
			return
		
		self.current_source_outpath = node.outpath

		for header in node.deps:
			self.visit(header)

			if isStale(header):
				self.markStale(node)
				return

		self.current_source_outpath = None


	def visitHeaderNode(self, node: HeaderNode):
		
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)
		else:
			return

		if self.current_source_outpath is None:
			raise RuntimeError("Source path should not have been None. Unexpected.")
		
		if self.current_source_outpath.stat().st_mtime < node.filepath.stat().st_mtime:
			markStale(node)
			return
		
		for header in node.deps:
			self.visit(header)

			if isStale(header):
				markStale(node)
				return

