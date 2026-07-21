from zero.compilers.get import getCompiler
from zero.graph.nodes import *
from zero.compilers import BaseCompiler


from zero.interface.build import Build
from zero.interface.executable import Executable
from zero.interface.source import Source
from zero.interface.lib import Library
from zero.interface.static_lib import StaticLibrary
from zero.interface.shared_lib import SharedLibrary
from zero.interface.precomp_lib import PreCompiledLibrary

from zero.reporter import getReporter


class GraphConstructor:

	def __init__(
			self, 
			root_compiler: str,
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
		self.made_ompiled_libs: dict[PreCompiledLibrary, PreCompiledLibraryNode] = {}

		self.build_dir = build_dir
		self.object_dir = object_dir
		self.exec_dir = exec_dir
		self.static_lib_dir = static_lib_dir
		self.shared_lib_dir = shared_lib_dir

		self.include_dirs: list[Path] = []

		self.root_compiler = getCompiler(root_compiler)
		self.current_compiler = self.root_compiler
		

	def makeRoot(self, build: Build) -> RootNode:
		targets = [self.makeTargetNode(t) for t in build._targets]
		targets = []
		compilers = {}

		for t in build._targets:
			if t.compiler == "inherit":
				self.current_compiler = self.root_compiler
			else:
				self.current_compiler = getCompiler(t.compiler)
				
			node = self.makeTargetNode(t)
			targets.append(node)
			compilers[node] = self.current_compiler

		root = RootNode(
			targets,
			compilers
			)
		
		return root
	

	def makeTargetNode(self, target) -> TargetNode:

		if isinstance(target, Executable):
			return self.makeExecutableNode(target)
		elif isinstance(target, StaticLibrary):
			return self.makeStaticLibraryNode(target)
		elif isinstance(target, SharedLibrary):
			return self.makeSharedLibraryNode(target)
		else:
			raise RuntimeError("What")


	def makeLibraryNode(self, lib: Library) -> LibraryNode:

		if isinstance(lib, PreCompiledLibrary):
			return self.makePrecompiledLibNode(lib)
		elif isinstance(lib, StaticLibrary):
			return self.makeStaticLibraryNode(lib)
		elif isinstance(lib, SharedLibrary):
			return self.makeSharedLibraryNode(lib)
		else:
			raise RuntimeError("What")


	def makeExecutableNode(self, exe: Executable) -> ExecutableNode:
		
		if exe in self.made_executables:
			return self.made_executables[exe]
		
		outfile = self.exec_dir / exe.name
		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for lib in exe._linked_libs:
			lib_node = self.makeLibraryNode(lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(exe.headers.private)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(exe.source)

		node = ExecutableNode(
			outfile,
			source_nodes,
			lib_nodes,
			exe._arguments,
			exe.headers.private
		)

		self.made_executables[exe] = node

		return node
	


	def makeStaticLibraryNode(self, lib: StaticLibrary) -> StaticLibraryNode:
		
		if lib in self.made_static_libs:
			return self.made_static_libs[lib]
		
		outfile = self.static_lib_dir / ("lib" + lib.name + ".a")

		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(lib.source)
		
		node = StaticLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib._arguments,
			lib.headers.private,
			lib.headers.public
		)

		self.made_static_libs[lib] = node
		
		return node
	

	def makeSharedLibraryNode(self, lib: SharedLibrary) -> SharedLibraryNode:

		if lib in self.made_shared_libs:
			return self.made_shared_libs[lib]
		
		outfile = self.shared_lib_dir / ("lib" + lib.name + ".so")

		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(lib.source)
		
		node = SharedLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib._arguments,
			lib.headers.private,
			lib.headers.public
		)

		self.made_shared_libs[lib] = node
		
		return node


	def makePrecompiledLibNode(self, lib: PreCompiledLibrary) -> PreCompiledLibraryNode:
		return PreCompiledLibraryNode(
			lib.filepath,
			lib.headers.public
		)


	def makeHeaderNode(self, path: Path) -> HeaderNode:

		if path in self.visited_headers:
			return self.visited_headers[path]
		
		header = HeaderNode(
			path,
			[]
		)
		self.visited_headers[path] = header

		deps = self.current_compiler.getDependencies(path, include_dirs=self.include_dirs) 
		included_headers = [self.makeHeaderNode(d) for d in deps]

		header.deps = included_headers
		
		return header
			

	def _makeSourceNode(self, path: Path) -> SourceNode:

		if path in self.visited_sources:
			return self.visited_sources[path]
		
		outfile = self.object_dir / path.parent / (path.name + ".o")

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			[]
		)

		self.visited_sources[path] = source

		deps = self.current_compiler.getDependencies(path, include_dirs=self.include_dirs) 
		included_headers = [self.makeHeaderNode(d) for d in deps]

		source.deps = included_headers

		return source
	

	def makeSourceNodes(self, source: Source) -> list[SourceNode]:
		return [self._makeSourceNode(p) for p in source._sources_paths]