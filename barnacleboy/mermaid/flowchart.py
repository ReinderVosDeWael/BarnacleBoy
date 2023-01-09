""" Module for building mermaid flowcharts. """
from enum import Enum
from typing import List, Optional, Any

from barnacleboy.mermaid.base import MermaidBase
from barnacleboy.mermaid.utils import generate_node_ids, init_string


class Orientation(Enum):
    """Orientation of the graph."""

    TB: str = "TB"
    TOP_BOTTOM: str = "TB"

    TD: str = "TD"
    TOP_DOWN: str = "TD"

    BT: str = "BT"
    BOTTOM_TOP: str = "BT"

    RL: str = "RL"
    RIGHT_LEFT: str = "RL"

    LR: str = "LR"
    LEFT_RIGHT: str = "LR"


class RelationshipStyles(Enum):
    """The type of relationship between two nodes."""

    SOLID: str = "---"
    DOTTED: str = "-.-"
    THICK: str = "==="


class NodeShape(Enum):
    """The shape of a node. $1 denotes where text will be inserted."""

    ROUNDED: str = "($1)"
    STADIUM: str = "([$1])"
    SUBROUTINE: str = "[[$1]]"
    CYLINDRICAL: str = "[($1)]"
    CIRCLE: str = "(($1))"
    ASYMMETRIC: str = ">$1]"
    RHOMBUS: str = "{$1}"
    HEXAGON: str = "{{$1}}"
    PARALLELOGRAM: str = "[/$1/]"
    PARALLELOGRAM_ALT: str = r"[\$1\]"
    TRAPEZOID: str = r"[/$1\]"
    TRAPEZOID_ALT: str = r"[\$1/]"
    DOUBLE_CIRCLE: str = "((($1)))"


class Node:
    """A node in a flowchart."""

    def __init__(self, name: str, shape: NodeShape = NodeShape.ROUNDED):
        """Initialize a node.

        Args:
            name: The name of the node.
            shape: The shape of the node.

        """
        self.name = name
        self.shape = shape
        self.internal_id: str = ""

    @property
    def node_string(self) -> str:
        """The string representation of the node."""
        return self.internal_id + self.shape.value.replace("$1", self.name)

    def __str__(self) -> str:
        return self.node_string


class Relationship:
    """A relationship between two nodes."""

    def __init__(
        self,
        nodes: List[Node],
        *,
        style: str = "SOLID",
        input_arrow: Optional[str] = None,
        output_arrow: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """Initialize a relationship.

        Args:
            nodes: The nodes to connect.
            style: The style of the relationship.
            input_arrow: The input arrow, valid values are "<", "o", "x"
            output_arrow: The output arrow, valid values are ">", "o", "x"
            label: The label of the relationship.
        """
        self.nodes = nodes
        self.style = style
        self.input_arrow = input_arrow
        self.output_arrow = output_arrow
        self.label = label

        if len(self.nodes) != 2:
            raise ValueError("A relationship must have exactly two nodes.")

    def get_relationship_string(self) -> str:
        """Generate a relationship string for a node."""
        output_string = ""
        output_string += self.nodes[0].internal_id
        if self.input_arrow:
            output_string += self.input_arrow
        output_string += RelationshipStyles[self.style].value
        if self.output_arrow:
            output_string += self.output_arrow
        if self.label:
            output_string += f"|{self.label}|"
        output_string += self.nodes[1].internal_id

        return output_string

    @property
    def relationship_string(self) -> str:
        """Property for accessing the relationship string of a node."""
        return self.get_relationship_string()

    def __str__(self) -> str:
        return self.relationship_string


class Flowchart(MermaidBase):
    """Base class for a flowchart."""

    def __init__(
        self,
        nodes: Optional[List[Node]] = None,
        relationships: Optional[List[Relationship]] = None,
        orientation: Orientation = Orientation.TB,
        title: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize a flowchart.

        Args:
            nodes: A list of nodes in the flowchart.
            relationships: A list of relationships between nodes in the flowchart.
            orientation: The orientation of the flowchart, defaults to "TB".
            title: The title of the flowchart.

        """
        super(Flowchart, self).__init__(**kwargs)
        self.nodes = nodes or []
        self.relationships = relationships or []
        self.orientation = orientation
        self.title = title
        self.config = {}

        self.set_node_ids()

    def create_node(self, *args: Any, **kwargs: Any) -> Node:
        """Create a node.

        Args:
            *args: Positional arguments to pass to the Node constructor.
            **kwargs: Keyword arguments to pass to the Node constructor.

        Returns:
            The created node.
        """
        node = Node(*args, **kwargs)
        self.add_nodes([node])
        return node

    def create_relationship(self, *args: Any, **kwargs: Any) -> Relationship:
        """Create a relationship between two nodes.

        Args:
            *args: Positional arguments to pass to the Relationship constructor.
            **kwargs: Keyword arguments to pass to the Relationship constructor.

        Returns:
            The created relationship.

        """
        relationship = Relationship(*args, **kwargs)
        self.add_relationships([relationship])
        return relationship

    def add_nodes(self, nodes: List[Node]) -> None:
        """Add a list of nodes to the flowchart.

        Args:
            nodes: A list of nodes to add to the flowchart.
        """
        for node in nodes:
            self.nodes.append(node)
        self.set_node_ids()

    def add_relationships(self, relationships: List[Relationship]) -> None:
        """Add a relationship between two nodes.

        Args:
            relationships: Relationships between the two nodes.

        """
        for relationship in relationships:
            if len(relationship.nodes) != 2:
                raise ValueError("A relationship must have exactly two nodes.")

            for node in relationship.nodes:
                if node not in self.nodes:
                    raise ValueError(
                        "Relationships must be between nodes in the flowchart."
                    )

        self.relationships += relationships

    def set_node_ids(self) -> None:
        """Set the internal IDs of the nodes."""
        node_ids = generate_node_ids(len(self.nodes))
        for node, node_id in zip(self.nodes, node_ids):
            node.internal_id = node_id

    def get_flowchart_string(self) -> str:
        """Generate a flowchart string."""
        output_string = init_string(self.base_config, self.config)
        if self.title:
            output_string += f"---\ntitle: {self.title}\n---\n"
        output_string += f"graph {self.orientation.value}\n"

        for node in self.nodes:
            output_string += f"    {node}\n"

        output_string += "\n"

        for relationship in self.relationships:
            output_string += f"    {relationship}\n"

        return output_string

    def __str__(self) -> str:
        """Return the flowchart string."""
        return self.get_flowchart_string()
