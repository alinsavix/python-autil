"""
argparse - A few helper functions that can be used with argparse to do
things we frequently need to do.
"""
import argparse
from pathlib import Path
from typing import Any, Optional, Sequence, Set, Text, Type, Union


def CheckFile(extensions: Optional[Set[str]] = None, must_exist: bool = False) -> Type[argparse.Action]:
    class Act(argparse.Action):
        def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                     values: Any, option_string: Optional[Text] = "") -> None:
            if not isinstance(values, Path):
                parser.error(
                    f"CheckFile called but argument is {type(values)} and not a pathlib path? (bug)")

            if extensions:
                ext = values.suffix[1:]
                if ext not in extensions:
                    # option_string = '({})'.format(option_string) if option_string else ''
                    parser.error(f"file '{values}' doesn't end with one of {extensions}")

            if must_exist:
                if not values.exists():
                    parser.error(f"file '{values}' does not exist")

            setattr(namespace, self.dest, values)

    return Act


class NegateAction(argparse.Action):
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[Text, Sequence[Any], None], option_string: Optional[Text] = "") -> None:
        if option_string is None:
            parser.error("NegateAction can only be used with non-positional arguments")

        # assert option_string is not None
        setattr(namespace, self.dest, option_string[2:4] != 'no')
