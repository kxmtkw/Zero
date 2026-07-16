from pathlib import Path
import subprocess


class Compiler:

	def __init__(self) -> None:
		pass


	def _parse_dependencies(self, gcc_output: str) -> list[str]:
		cleaned = gcc_output.replace("\\\n", " ").replace("\\", " ")
		
		if ":" not in cleaned:
			return []
		
		_, deps_part = cleaned.split(":", 1)
		
		filepaths = deps_part.strip().split()
		filepaths.pop(0)
		
		return filepaths


	def get_dependencies(self, filepath: str) -> list[str]:

		process = subprocess.run(["gcc", "-MM", filepath], capture_output=True, text=True)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)
		
		files = self._parse_dependencies(process.stdout)
		return files


	def build_file(self, filepath: Path, outfile: Path):  
		process = subprocess.run(["gcc", "-c", str(filepath), "-o", str(outfile)], capture_output=True, text=True)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)
		

	def link(self, outfile: Path, *objects: Path):  
		process = subprocess.run(["gcc", *[str(o) for o in objects], "-o", str(outfile)], capture_output=True, text=True)

		if process.returncode != 0:
			raise RuntimeError(process.stderr)