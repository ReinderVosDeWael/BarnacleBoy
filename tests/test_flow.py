from src.mermaid.flowchart import Flowchart, Node, Orientation, NodeShape, Relationship


def test_create_node():
    node = Node("Anakin Skywalker")

    assert node.name == "Anakin Skywalker"
    assert node.shape == NodeShape.ROUNDED


def test_create_relationship():
    node = Node("Anakin Skywalker")
    node2 = Node("Darth Vader")

    relationship = Relationship([node, node2], label="Turns to the dark side")

    assert relationship.nodes == [node, node2]
    assert relationship.label == "Turns to the dark side"


def test_flowchart():
    """Test the flowchart class."""
    flowchart = Flowchart()
    anakin = flowchart.create_node("Anakin Skywalker")
    vader = flowchart.create_node("Darth Vader")
    relationship = flowchart.create_relationship(
        [anakin, vader], label="Turns to the dark side"
    )

    assert flowchart.nodes == [anakin, vader]
    assert flowchart.relationships == [relationship]
    assert flowchart.orientation == Orientation.TB
    assert (
        str(flowchart)
        == "graph TB\n    A(Anakin Skywalker)\n    B(Darth Vader)\n\n    A--->|Turns to the dark side|B"
    )
