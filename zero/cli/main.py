from zero.orchestrator import Orchestrator
from zero.cli.args import setupParser, parseArguments


def main():
	parser = setupParser()
	args = parseArguments(parser)

	orchestrator = Orchestrator()

	if args.command == "make":
		if len(args.target) == 0:
			orchestrator.makeBuild(fresh=args.fresh)
		else:
			orchestrator.makeTargets(args.target, fresh=args.fresh)


