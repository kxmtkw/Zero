from pathlib import Path
import subprocess
from .base import BaseCompiler


class Clang(BaseCompiler):


    def __init__(self) -> None:
        super().__init__()


    def _parse_dependencies(self, clang_output: str) -> list[Path]:
        cleaned = clang_output.replace("\\\n", " ").replace("\\", " ")
        
        if ":" not in cleaned:
            return []
        
        _, deps_part = cleaned.split(":", 1)
        filepaths = deps_part.strip().split()
        filepaths.pop(0)  
        
        return [Path(p) for p in filepaths]


    def get_dependencies(self, filepath: Path) -> list[Path]:

        process = subprocess.run(
            ["clang", "-MM", str(filepath)], 
            capture_output=True, 
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(process.stderr)
        
        return self._parse_dependencies(process.stdout)


    def build_file(self, filepath: Path, outfile: Path) -> None:  

        process = subprocess.run(
            ["clang", "-c", str(filepath), "-o", str(outfile)], 
            capture_output=True, 
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(process.stderr)


    def link(self, objects: list[Path], outfile: Path) -> None:  

        str_objects = [str(obj) for obj in objects]
        process = subprocess.run(
            ["clang", *str_objects, "-o", str(outfile)], 
            capture_output=True, 
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(process.stderr)