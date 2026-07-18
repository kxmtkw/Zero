from pathlib import Path

class Node():

	def __init__(self):
		pass


class TargetNode(Node):

	def __init__(self, outfile: Path, sources: list[SourceNode], libs: list[LibraryNode]):
		super().__init__()
		self.outfile: Path = outfile
		self.sources: list[SourceNode] = sources
		self.linked_libraries: list[LibraryNode] = libs


class LibraryNode(TargetNode):

	def __init__(self, outfile: Path, sources: list[SourceNode], libs: list[LibraryNode]):
		super().__init__(outfile, sources, libs)


class StaticLibraryNode(LibraryNode):

	def __init__(self, outfile: Path, sources: list[SourceNode], libs: list[LibraryNode]):
		super().__init__(outfile, sources, libs)


class SharedLibraryNode(LibraryNode):

	def __init__(self, outfile: Path, sources: list[SourceNode], libs: list[LibraryNode]):
		super().__init__(outfile, sources, libs)


class ExecutableNode(TargetNode):

	def __init__(self, outfile: Path, sources: list[SourceNode], libs: list[LibraryNode]):
		super().__init__(outfile, sources, libs)


class FileNode(Node):

	def __init__(self, filepath: Path):
		super().__init__()
		self.filepath: Path = filepath

		
class SourceNode(FileNode):
	def __init__(self, filepath: Path, outfile: Path, sources: list[HeaderNode]):
		super().__init__(filepath)
		self.sources: list[HeaderNode] = sources
		self.outfile: Path = outfile


class HeaderNode(FileNode):
	def __init__(self, filepath: Path, sources: list[HeaderNode]):
		super().__init__(filepath)
		self.sources: list[HeaderNode] = sources


class RootNode(Node):

	def __init__(self, targets: list[TargetNode]):
		super().__init__()
		self.targets: list[TargetNode] = targets