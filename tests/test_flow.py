from barnacleboy.mermaid.flowchart import (
    Flowchart,
    Node,
    NodeShape,
    Relationship,
)


def test_create_node():
    node = Node("Anakin Skywalker")

    assert node.name == "Anakin Skywalker"
    assert node.shape == NodeShape.ROUNDED


def test_create_relationship():
    node = Node("Anakin Skywalker")
    node2 = Node("Darth Vader")

    relationship = Relationship([node, node2], label="Turns to the dark side")

    assert relationship.entities == [node, node2]
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
    assert flowchart.orientation == "TB"

    assert (
        str(flowchart)
        == "graph TB\n    A(Anakin Skywalker)\n    B(Darth Vader)\n\n    A---|Turns to the dark side|B\n"
    )


def test_flowchart_with_subgraph():
    """Test the flowchart class."""
    flowchart = Flowchart()
    anakin = flowchart.create_node("Anakin Skywalker")
    vader = flowchart.create_node("Darth Vader")
    sidious = flowchart.create_node("Darth Sidious")
    obiwan = flowchart.create_node("Obi-Wan Kenobi")

    relationship = flowchart.create_relationship(
        [anakin, vader], label="Turns to the dark side"
    )

    dark_subgraph = flowchart.create_subgraph("The Dark Side", [vader, sidious])
    light_subgraph = flowchart.create_subgraph("The Light Side", [anakin, obiwan])
    all_subgraph = flowchart.create_subgraph("All", [dark_subgraph, light_subgraph])

    assert flowchart.nodes == [anakin, vader, sidious, obiwan]
    assert flowchart.relationships == [relationship]
    assert flowchart.orientation == "TB"
    assert flowchart.subgraphs == [dark_subgraph, light_subgraph, all_subgraph]
    assert (
        str(flowchart)
        == "graph TB\n    subgraph G [All]\ndirection TB\nsubgraph E [The Dark Side]\ndirection TB\nB(Darth Vader)\nC(Darth Sidious)\nend\n\nsubgraph F [The Light Side]\ndirection TB\nA(Anakin Skywalker)\nD(Obi-Wan Kenobi)\nend\n\nend\n\n\n    A---|Turns to the dark side|B\n"
    )
