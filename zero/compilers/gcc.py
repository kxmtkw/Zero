from pathlib import Path
import subprocess
from .base import BaseCompiler


class Gcc(BaseCompiler):


	def __init__(self) -> None:
		super().__init__()


	def _parse_dependencies(self, gcc_output: str) -> list[Path]:
		cleaned = gcc_output.replace("\\\n", " ").replace("\\", " ")
		
		if ":" not in cleaned:
			return []
		
		_, deps_part = cleaned.split(":", 1)
		filepaths = deps_part.strip().split()
		filepaths.pop(0)
		
		return [Path(p) for p in filepaths]


	def get_dependencies(self, filepath: Path) -> list[Path]:

		process = subprocess.run(
			["gcc", "-MM", str(filepath)], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)
		
		return self._parse_dependencies(process.stdout)


	def build_file(self, filepath: Path, outfile: Path, *, for_shared = False) -> None:  

		process = subprocess.run(
			["gcc", "-c", "-fPIC" if for_shared else "", str(filepath), "-o", str(outfile)], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)

		
	def build_static_lib(self, objects: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]

		process = subprocess.run(
			["ar", "rcs", str(outfile), *str_objects], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)
		

	def build_shared_lib(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]
		
		cmd = ["gcc", "-shared", "-o", str(outfile), *str_objects]
		
		if libraries:
			cmd.append("-Wl,--whole-archive")
			for lib in libraries:
				cmd.append(str(lib))
			cmd.append("-Wl,--no-whole-archive")

		process = subprocess.run(
			cmd, 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)


	def build_executable(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]
		str_libs = [str(lib) for lib in libraries]

		process = subprocess.run(
			["gcc", *str_objects, *str_libs, "-o", str(outfile)], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)