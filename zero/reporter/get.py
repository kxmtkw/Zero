from .reporter import TerminalReporter


def getReporter() -> TerminalReporter:
	"Get the currently intialized reporter."
	if TerminalReporter._instance:
		return TerminalReporter._instance
	else:
		return TerminalReporter()