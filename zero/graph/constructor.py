
from zero.nodes.nodes import *
from zero.compilers import BaseCompiler


from zero.interface.build import Build
from zero.interface.executable import Executable
from zero.interface.source import Source
from zero.interface.lib import Library
from zero.interface.static_lib import StaticLibrary
from zero.interface.shared_lib import SharedLibrary



class GraphConstructor:

	def __init__(
			self, 
			compiler: BaseCompiler, 
			build_dir: Path,
			object_dir: Path,
			exec_dir: Path,
			static_lib_dir: Path,
			shared_lib_dir: Path
			) -> None:

		self.visited_headers: dict[Path, HeaderNode] = {}
		self.visited_sources: dict[Path, SourceNode] = {}

		self.made_executables: dict[Executable, ExecutableNode] = {}
		self.made_static_libs: dict[StaticLibrary, StaticLibraryNode] = {}
		self.made_shared_libs: dict[SharedLibrary, SharedLibraryNode] = {}

		self.compiler = compiler

		self.build_dir = build_dir
		self.object_dir = object_dir
		self.exec_dir = exec_dir
		self.static_lib_dir = static_lib_dir
		self.shared_lib_dir = shared_lib_dir

		self.include_dirs: list[Path] = []
		

	def make_root(self, build: Build) -> RootNode:
		
		targets: list[TargetNode] = []

		for t in build._targets:
			if isinstance(t, Executable):
				targets.append(self.make_executable_node(t))
			elif isinstance(t, Library):
				targets.append(self.make_library_node(t))


		return RootNode(targets)
	

	def make_header_node(self, path: Path) -> HeaderNode:

		if path in self.visited_headers:
			return self.visited_headers[path]
		
		deps = self.compiler.get_dependencies(path, include_dirs=self.include_dirs)	
		included_headers = [self.make_header_node(d) for d in deps]

		header = HeaderNode(
			path,
			included_headers
		)
		self.visited_headers[path] = header
		return header
			

	def _make_source_node(self, path: Path) -> SourceNode:

		if path in self.visited_sources:
			return self.visited_sources[path]
		
		deps = self.compiler.get_dependencies(path, include_dirs=self.include_dirs)	
		included_headers = [self.make_header_node(d) for d in deps]

		outfile = self.object_dir / path.parent / (path.name + ".o")

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			included_headers
		)

		self.visited_sources[path] = source

		return source
	

	def make_source_nodes(self, source: Source) -> list[SourceNode]:
		return [self._make_source_node(p) for p in source._sources_paths]
	

	def make_executable_node(self, exe: Executable) -> ExecutableNode:
		
		if exe in self.made_executables:
			return self.made_executables[exe]
		
		outfile = self.exec_dir / exe.name
		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for lib in exe._linked_libs:
			lib_node = self.make_library_node(lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)		
		
		include_dirs.extend(exe.headers.private)

		self.include_dirs = include_dirs

		source_nodes = self.make_source_nodes(exe.source)

		node = ExecutableNode(
			outfile,
			source_nodes,
			lib_nodes,
			exe.headers.private
		)

		self.made_executables[exe] = node

		return node
	

	def make_library_node(self, lib: Library) -> LibraryNode:
		if isinstance(lib, StaticLibrary):
			return self.make_static_library_node(lib)
		elif isinstance(lib, SharedLibrary):
			return self.make_shared_library_node(lib)
		else:
			raise RuntimeError("What")


	def make_static_library_node(self, lib: StaticLibrary) -> StaticLibraryNode:
		
		if lib in self.made_static_libs:
			return self.made_static_libs[lib]
		
		outfile = self.static_lib_dir / ("lib" + lib.name + ".a")

		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.make_library_node(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)		
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.make_source_nodes(lib.source)
		
		node = StaticLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib.headers.private,
			lib.headers.public
		)

		self.made_static_libs[lib] = node
		
		return node
	

	def make_shared_library_node(self, lib: SharedLibrary) -> SharedLibraryNode:

		if lib in self.made_shared_libs:
			return self.made_shared_libs[lib]
		
		outfile = self.shared_lib_dir / ("lib" + lib.name + ".so")

		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.make_library_node(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)		
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.make_source_nodes(lib.source)
		
		node = SharedLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib.headers.private,
			lib.headers.public
		)

		self.made_shared_libs[lib] = node
		
		return node


