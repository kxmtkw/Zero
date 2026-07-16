from pathlib import Path
import subprocess



def parse_dependencies(gcc_output: str) -> list[str]:
    cleaned = gcc_output.replace("\\\n", " ").replace("\\", " ")
    
    if ":" not in cleaned:
        return []
    
    _, deps_part = cleaned.split(":", 1)
    
    filepaths = deps_part.strip().split()
    
    return filepaths


def get_dependencies(filepath: Path) -> list[Path]:

	process = subprocess.run(["gcc", "-MM", str(filepath)], capture_output=True, text=True)

	if process.returncode != 0:
		raise RuntimeError(process.stderr)
	
	files = parse_dependencies(process.stdout)

	return [Path(file) for file in files]


def build_file(filepath: Path, outfile: Path):  
	process = subprocess.run(["gcc", "-c", str(filepath), "-o", str(outfile)], capture_output=True, text=True)

	if process.returncode != 0:
		raise RuntimeError(process.stderr)
	

def link_exes(outfile: Path, *objects: Path):  
	process = subprocess.run(["gcc", *[str(o) for o in objects], "-o", str(outfile)], capture_output=True, text=True)

	if process.returncode != 0:
		raise RuntimeError(process.stderr)