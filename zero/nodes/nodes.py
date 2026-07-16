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

	def __hash__(self) -> int:
		return hash(str(self.filepath.absolute()))

		
class SourceNode(FileNode):

	def __init__(self, filepath: Path, deps: list[HeaderNode]):
		super().__init__(filepath)
		self.dependencies: list[HeaderNode] = deps
		self.outfile: Path


class HeaderNode(FileNode):

	def __init__(self, filepath: Path, deps: list[HeaderNode]):
		super().__init__(filepath)
		self.dependencies: list[HeaderNode] = deps


class RootNode(Node):
	"Class to represent a whole build project."

	def __init__(self, targets: list[TargetNode]):
		super().__init__()
		self.targets = targets