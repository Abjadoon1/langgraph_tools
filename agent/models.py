from dataclasses import dataclass, field
from collections.abc import Callable


@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    parameters: dict[str, int | float | str] = field(default_factory=dict)

    def execute(self, *args, **kwargs):
        return self.function(*args, **kwargs)
