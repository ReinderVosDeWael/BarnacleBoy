from barnacleboy.mermaid.piechart import Piechart


def test_piechart():
    """Test the piechart class."""
    piechart = Piechart("Delicacies", {"Bantha Fodder": 9, "Jawa Juice": 5})

    assert (
        str(piechart) == 'pie title Delicacies\n"Bantha Fodder": 9\n"Jawa Juice": 5\n'
    )
