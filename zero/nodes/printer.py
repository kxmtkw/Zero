from .nodes import *
from .visitor import NodeVisitor


class NodePrinter(NodeVisitor):


    def __init__(self) -> None:
        super().__init__()
        self._depth: int = 0
        self._visited_ids: set[int] = set()


    def _get_indent(self) -> str:
        return "    " * self._depth


    def _print_node_base(self, node: Node, label: str, details: str) -> bool:
        hex_id = f"0x{id(node):0x}"
        indent = self._get_indent()
        
        if id(node) in self._visited_ids:
            print(f"{indent}[{label}] {details} -> see {hex_id}")
            return True
            
        self._visited_ids.add(id(node))
        print(f"{indent}[{label}] {details} ({hex_id})")
        return False


    def visitRootNode(self, node: RootNode):
        if self._print_node_base(node, "Root", f"{len(node.targets)} targets"):
            return
            
        self._depth += 1
        for target in node.targets:
            self.visit(target)
        self._depth -= 1


    def visitExecutableNode(self, node: ExecutableNode):
        if self._print_node_base(node, "Executable", str(node.outfile)):
            return
            
        self._depth += 1
        for src in node.sources:
            self.visit(src)
        for lib in node.linked_libraries:
            self.visit(lib)
        self._depth -= 1


    def visitStaticLibraryNode(self, node: StaticLibraryNode):
        if self._print_node_base(node, "StaticLibrary", str(node.outfile)):
            return
            
        self._depth += 1
        for src in node.sources:
            self.visit(src)
        for lib in node.linked_libraries:
            self.visit(lib)
        self._depth -= 1


    def visitSharedLibraryNode(self, node: SharedLibraryNode):
        if self._print_node_base(node, "SharedLibrary", str(node.outfile)):
            return
            
        self._depth += 1
        for src in node.sources:
            self.visit(src)
        for lib in node.linked_libraries:
            self.visit(lib)
        self._depth -= 1
    

    def visitSourceNode(self, node: SourceNode):
        details = f"{node.filepath} -> {node.outfile}"
        if self._print_node_base(node, "Source", details):
            return
            
        self._depth += 1
        for header in node.headers:
            self.visit(header)
        self._depth -= 1


    def visitHeaderNode(self, node: HeaderNode):
        if self._print_node_base(node, "Header", str(node.filepath)):
            return
            
        self._depth += 1
        for header in node.headers:
            self.visit(header)
        self._depth -= 1