from zero.nodes.nodes import *
from zero.compilers import BaseCompiler


from zero.interface.build import Build
from zero.interface.executable import Executable
from zero.interface.source import Source
from zero.interface.static_lib import StaticLibrary


class GraphConstructor:


	def __init__(self, compiler: BaseCompiler, build_dir: Path) -> None:
		self.visited_headers: dict[Path, HeaderNode] = {}
		self.compiler = compiler
		self.build_dir = build_dir

		self.objects_dir = build_dir / "objects"
		if not self.objects_dir.exists():
			self.objects_dir.mkdir()


	def make_root(self, build: Build) -> RootNode:
		
		targets: list[TargetNode] = []

		for t in build._targets:
			if isinstance(t, Executable):
				targets.append(self.make_executable_node(t))
			elif isinstance(t, StaticLibrary):
				targets.append(self.make_static_library_node(t))
	
		return RootNode(targets)
	

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
			

	def _make_source_node(self, path: Path) -> SourceNode:

		deps = self.compiler.get_dependencies(path)	
		included_headers = [self.make_header_node(d) for d in deps]

		outfile = self.objects_dir / path.parent / (path.name + ".o")

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			included_headers
		)

		return source
	

	def make_source_nodes(self, source: Source) -> list[SourceNode]:
		return [self._make_source_node(p) for p in source._sources_paths]

	

	def make_executable_node(self, exe: Executable) -> ExecutableNode:
		
		outfile = exe.outfile

		if not outfile:
			raise RuntimeError("no")
		
		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		node = ExecutableNode(
			outfile,
			self.make_source_nodes(exe.source),
			[self.make_static_library_node(lib) for lib in exe._linked_libs]
		)

		return node
	

	def make_static_library_node(self, lib: StaticLibrary) -> StaticLibraryNode:

		outfile = lib.outfile

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		node = StaticLibraryNode(
			outfile,
			self.make_source_nodes(lib.source),
			[self.make_static_library_node(lib) for lib in lib._linked_libs]
		)

		return node
	

	def make_shared_library_node(self, outfile: Path, sources: list[Path], libs: list[LibraryNode]) -> SharedLibraryNode:

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		lib = SharedLibraryNode(
			outfile,
			[self.make_source_node(s) for s in sources],
			libs
		)

		return lib


