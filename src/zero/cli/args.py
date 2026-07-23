import argparse
import sys


def add_make_command(subparsers: argparse._SubParsersAction) -> None:
	make_parser = subparsers.add_parser(
		"make",
		help="Build targets",
	)
	make_parser.add_argument(
		"--fresh",
		action="store_true",
		help="Force a clean rebuild",
	)
	make_parser.add_argument(
		"target",
		nargs="*",
		default=None,
		help="Target to build",
	)


def add_run_command(subparsers: argparse._SubParsersAction) -> None:
	run_parser = subparsers.add_parser(
		"run",
		help="Run executables",
	)
	run_parser.add_argument(
		"--fresh",
		action="store_true",
		help="Force a rebuild before running",
	)
	run_parser.add_argument(
		"executable",
		help="Path or name of the executable",
	)
	run_parser.add_argument(
		"executable_args",
		nargs=argparse.REMAINDER,
		help="Arguments passed directly to the executable",
	)


def setupParser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="zero", description="Zero build system")
	subparsers = parser.add_subparsers(dest="command", required=True)

	add_make_command(subparsers)
	add_run_command(subparsers)

	return parser


def parseArguments(
	parser: argparse.ArgumentParser, args: list[str] | None = None
) -> argparse.Namespace:
	if args is None:
		args = sys.argv[1:]

	return parser.parse_args(args)