import functools
import inspect
from pathlib import Path
from typing import Any, Callable, List

TFunc = Callable[..., Any]

def fix_path(func: TFunc) -> TFunc:
    functools.wraps(func)

    def inner(*args: Any, **kwargs: Any) -> Any:
        # spec = inspect.getfullargspec(func)
        # print(spec)

        sig = inspect.signature(func)
        # print(sig.parameters)
        # print(f"args in: {args}")

        _args: List[Any] = []
        for name, val in zip(sig.parameters, args):
            if sig.parameters[name].annotation == Path:
                _args.append(Path(val))
            else:
                _args.append(val)
        # print(f"args out: {_args}")

        # print(f"kwargs in: {kwargs}")
        for argname, argvalue in kwargs.items():
            if argname in sig.parameters and sig.parameters[argname].annotation == Path:
                kwargs[argname] = Path(argvalue)
        # print(f"kwargs out: {kwargs}")

        return func(*_args, **kwargs)

    return inner


if __name__ == "__main__":
    @fix_path
    def thingie(path: Path, path2: str, int1: int, path3, path4: Path) -> None:
        print(f"path: {type(path)}")
        print(f"path2: {type(path2)}")
        print(f"path3: {type(path3)}")
        print(f"path4: {type(path4)}")
        print(f"int1: {type(int1)}")


    # thingie(path="/tmp/path", path4="/tmp/path4", path3="/tmp/path3", path2="/tmp/path2")
    thingie("/tmp/path", 2, 14, path3="/tmp/path3", path4="/tmp/path4")
