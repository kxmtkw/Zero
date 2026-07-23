from pathlib import Path
import subprocess


class Executor:

	def __init__(self) -> None:
		pass

	def run(self, cmd: str, arguments: list[str]):
		subprocess.run(
			[cmd, *arguments],
			capture_output=False,
		)