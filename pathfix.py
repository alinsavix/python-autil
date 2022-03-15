import functools
import inspect
from pathlib import Path
from typing import Any, Callable, List

TFunc = Callable[..., Any]

def fix_path(func: TFunc) -> TFunc:
    functools.wraps(func)

    def inner(*args: Any) -> Any:
        sig = inspect.signature(func)
        _args: List[Any] = []
        for name, val in zip(sig.parameters, args):
            if sig.parameters[name].annotation == Path:
                _args.append(Path(val))
            else:
                _args.append(val)
        res = func(*_args)
        return res
    return inner


if __name__ == "__main__":
    @fix_path
    def thingie(path: Path, path2: str, path3, path4: Path) -> None:
        print(f"path: {type(path)}")
        print(f"path2: {type(path2)}")
        print(f"path3: {type(path3)}")
        print(f"path4: {type(path4)}")


    # thingie(path="/tmp/path", path4="/tmp/path2", path3="/tmp/path3", path2="/tmp/path4")
    thingie("/tmp/path", "/tmp/path2", "/tmp/path3", "/tmp/path4")
