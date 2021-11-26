# file: app/command.py

import sys
import argparse

class Command:

	def __init__(self, description = None, usage = None):
		self.description = description
		self.usage = usage

		self.parser = argparse.ArgumentParser(description=self.description, usage=self.usage)
		self.subparsers = self.parser.add_subparsers(dest="subcommand")

	def argument(self, *name_or_flags, **kwargs):
		return name_or_flags, kwargs

	def command(self, *parser_args):
		def decorator(func):
			for args, kwargs in parser_args:
				self.parser.add_argument(*args, **kwargs)
			self.parser.set_defaults(func=func)
		return decorator

	def subcommand(self, *subparser_args):
		def decorator(func):
			parser = self.subparsers.add_parser(func.__name__, description=func.__doc__)
			for args, kwargs in subparser_args:
				parser.add_argument(*args, **kwargs)
			parser.set_defaults(func=func)
		return decorator

	def parse(self):
		if len(sys.argv) <= 1:
			self.parser.print_help()
		else:
			args = self.parser.parse_args()
			args.func(self, args)

	def printHelp(self):
		self.parser.print_help()
