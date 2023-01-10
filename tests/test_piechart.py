import tempfile
from pathlib import Path

from barnacleboy.mermaid.piechart import Piechart


def test_piechart():
    """Test the piechart class."""
    piechart = Piechart("Delicacies", {"Bantha Fodder": 9, "Jawa Juice": 5})

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        piechart.save(temp_file.name)

        assert Path(temp_file.name).exists()
