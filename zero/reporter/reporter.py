from rich.console import Console
from rich.status import Status


class TerminalReporter:
	"""
	Class for reporting build phases and logs to the terminal.
	"""

	_instance: TerminalReporter | None = None


	def __init__(self) -> None:
		self._console = Console()
		self._status: Status | None = None
		self._phase_name: str = ""

		if TerminalReporter._instance is None:
			TerminalReporter._instance = self


	def startPhase(self, phase_name: str, phase_verb: str):
		self._phase_name = phase_name
		self._console.print(f"[bold blue]── {self._phase_name}")
		self._status = self._console.status(f"[bold blue]{phase_verb}", spinner="dots")
		self._status.start()


	def endPhase(self, msg: str | None = None):
		if self._status:
			self._status.stop()

		if msg is not None:
			self._console.print(f"    [blue]└─ {msg}\n")

	
	def taskDone(self, task: str, msg: str):
		self._console.print(f"    [blue]│[/blue][green] {task:<16}[/green] {msg} ")


	def error(self, msg: str):
		self._console.print(f"[bold red]Error: {msg} [/bold red]")
	