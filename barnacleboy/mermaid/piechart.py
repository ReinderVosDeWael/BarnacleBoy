from barnacleboy.mermaid.base import MermaidBase


class Piechart(MermaidBase):
    def __init__(self, title: str, data: dict[str, int]) -> None:
        self.title = title
        self.data = data

    def get_piechart_string(self) -> str:
        """Get a string representation of the object."""
        output_string = f"pie title {self.title}\n"
        for key, value in self.data.items():
            output_string += f'"{key}": {value}\n'
        return output_string

    def __str__(self) -> str:
        return self.get_piechart_string()
