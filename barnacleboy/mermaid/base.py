import base64
from pathlib import Path
from typing import Union, Optional, Any

from pydantic import Field, BaseModel, Extra

from barnacleboy.config import get_settings

settings = get_settings()
VALID_THEMES = settings.VALID_THEMES
TEMPLATE_DIR = settings.TEMPLATE_DIR

COLOR_HEX_REGEX = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


class ThemeVariables(BaseModel):
    """Variables to alter the base theme."""

    darkMode: Optional[bool] = Field(None)
    background: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    fontFamily: Optional[str] = Field(None)
    fontSize: Optional[int] = Field(None, gt=0)
    primaryColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    primaryBorderColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    primaryTextColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    secondaryColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    secondaryBorderColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    tertiaryColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    tertiaryBorderColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    tertiaryTextColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    noteBkgColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    noteTextColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    noteBorderColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    lineColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    textColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    mainBkg: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    errorBkgColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)
    errorTextColor: Optional[str] = Field(None, regex=COLOR_HEX_REGEX)

    class Config:
        """Config for the theme variables."""

        extra = Extra.forbid


class MermaidBase:
    """Base class for mermaid objects. Provides methods for saving and rendering."""

    def __init__(self, theme: str = "base", **kwargs: Any) -> None:
        """Initialize a mermaid object."""
        if theme not in VALID_THEMES:
            raise ValueError(f"Theme {theme} is not supported.")
        if theme != "base" and kwargs:
            raise ValueError("Theme variables can only be set for the base theme.")

        self.theme = theme
        self.theme_variables = ThemeVariables(**kwargs)

    @property
    def base_config(self) -> dict[str, dict[str, str]]:
        """Get a dictionary representation of the init settings."""
        config = {
            "init": {
                "theme": self.theme,
            }
        }
        theme_variables = self.theme_variables.dict(exclude_none=True)
        if self.theme == "base" and theme_variables:
            config["init"]["themeVariables"] = theme_variables
        return config

    def save_html(self, filename: Union[str, Path]) -> None:
        filename = Path(filename)
        template = TEMPLATE_DIR / "mermaid_diagram.html"

        with open(template, "r") as file:
            html = file.read()
            html = html.replace("{{GRAPH}}", str(self))

        with open(filename, "w") as file:
            file.write(html)

    def jupyter_plot(self) -> None:
        """Render the graph in a Jupyter notebook.

        Notes:
            This method requires an internet connection.
        """
        if not self.is_notebook():
            raise RuntimeError("This method can only be used in a Jupyter notebook.")
        from IPython.display import Image, display  # type: ignore

        graphbytes = str(self).encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        display(Image(url="https://mermaid.ink/img/" + base64_string))

    @staticmethod
    def is_notebook() -> bool:
        """Check if the code is running in a Jupyter notebook."""
        try:
            shell = get_ipython().__class__.__name__  # type: ignore
            print(shell)
            return shell == "ZMQInteractiveShell"
        except NameError:
            return False
