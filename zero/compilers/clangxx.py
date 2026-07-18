from .gcc import GccCompiler

class ClangxxCompiler(GccCompiler):

	def __init__(self) -> None:
		super().__init__()
		self.compiler_binary = self.linker_binary = "clang++"
