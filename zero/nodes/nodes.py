from pathlib import Path

class Node():
	"Base node class for the build system"
	def __init__(self):
		pass


class TargetNode(Node):
	"Base class for representing targets like executables and libraries."
	def __init__(self):
		super().__init__()


class ExecutableNode(TargetNode):
	"Class for representing executables."

	def __init__(self, outfile: Path, deps: list[SourceNode]):
		super().__init__()
		self.outfile: Path = outfile
		self.dependencies: list[SourceNode] = deps


class FileNode(Node):

	def __init__(self, filepath: Path):
		super().__init__()
		self.filepath: Path = filepath

		
class SourceNode(FileNode):

	def __init__(self, filepath: Path, outfile: Path, deps: list[FileNode]):
		super().__init__(filepath)
		self.outfile: Path = outfile
		self.dependencies: list[FileNode] = deps


class HeaderNode(FileNode):

	def __init__(self, filepath: Path, deps: list[FileNode]):
		super().__init__(filepath)
		self.dependencies: list[FileNode] = deps

