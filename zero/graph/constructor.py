from zero.nodes.nodes import *
from zero.compilers import BaseCompiler


class GraphConstructor:


	def __init__(self, compiler: BaseCompiler, build_dir: Path) -> None:
		self.visited_headers: dict[Path, HeaderNode] = {}
		self.compiler = compiler
		self.build_dir = build_dir

		self.objects_dir = build_dir / "objects"
		if not self.objects_dir.exists():
			self.objects_dir.mkdir()


	
	def make_header_node(self, path: Path) -> HeaderNode:

		deps = self.compiler.get_dependencies(path)	
		included_headers = [self.make_header_node(d) for d in deps]

		if path in self.visited_headers:
			return self.visited_headers[path]
		else:
			header = HeaderNode(
				path,
				included_headers
			)
			self.visited_headers[path] = header
			return header
			

	def make_source_node(self, path: Path) -> SourceNode:

		deps = self.compiler.get_dependencies(path)	
		included_headers = [self.make_header_node(d) for d in deps]

		outfile = self.objects_dir / path.parent / (path.name + ".o")
		if not outfile.parent.exists():
			outfile.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			included_headers
		)

		return source
	

	def make_executable_node(self, outfile: Path, sources: list[Path]) -> ExecutableNode:

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)
			
		exe = ExecutableNode(
			outfile,
			[self.make_source_node(s) for s in sources]
		)

		
		return exe


