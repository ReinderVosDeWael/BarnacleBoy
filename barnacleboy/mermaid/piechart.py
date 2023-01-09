from typing import Any

from barnacleboy.mermaid.base import MermaidBase
from barnacleboy.mermaid.utils import init_string


class Piechart(MermaidBase):
    def __init__(self, title: str, data: dict[str, int], **kwargs: Any) -> None:
        """Initialize a piechart.

        Args:
            title: The title of the piechart.
            data: The data to be displayed in the piechart in the format {label: value}.
            kwargs: Additional keyword arguments to be passed to the MermaidBase class.
        """
        super(Piechart, self).__init__(**kwargs)
        self.title = title
        self.data = data
        self.config = {}

    def get_piechart_string(self) -> str:
        """Get a string representation of the object."""
        output_string = init_string(self.base_config, self.config)
        output_string += f"pie title {self.title}\n"
        for key, value in self.data.items():
            output_string += f'"{key}": {value}\n'
        return output_string

    def __str__(self) -> str:
        return self.get_piechart_string()
