""" Module for building mermaid flowcharts. """
from enum import Enum
from typing import List, Optional, Any, Union

from barnacleboy.mermaid.base import MermaidBase
from barnacleboy.mermaid.utils import (
    generate_internal_ids,
    init_string,
)


class Orientation(Enum):
    """Orientation of the graph."""

    TB: str = "TB"
    TOP_BOTTOM: str = "TB"

    BT: str = "BT"
    BOTTOM_TOP: str = "BT"

    RL: str = "RL"
    RIGHT_LEFT: str = "RL"

    LR: str = "LR"
    LEFT_RIGHT: str = "LR"


class RelationshipStyles(Enum):
    """The type of relationship between two entities."""

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
        self._internal_id: str = ""

    def __str__(self) -> str:
        """The string representation of the node."""
        return self._internal_id + self.shape.value.replace("$1", self.name)


class Subgraph:
    """A subgraph in a flowchart.

    Args:
        name: The name of the subgraph.
        nodes: The entities in the subgraph.

    """

    def __init__(self, name: str, nodes: List[Union[Node, "Subgraph"]]) -> None:
        self.name = name
        self.entities = nodes
        self._internal_id: str = ""
        self.direction: str = Orientation.TOP_BOTTOM.value

    def __str__(self) -> str:
        output_string = f"subgraph {self._internal_id} [{self.name}]\n"
        output_string += f"direction {self.direction}\n"
        nodes = [entity for entity in self.entities if isinstance(entity, Node)]
        subgraphs = [entity for entity in self.entities if isinstance(entity, Subgraph)]

        for node in nodes:
            output_string += f"{node}\n"

        for subgraph in subgraphs:
            output_string += f"{subgraph}\n"

        output_string += "end\n"
        return output_string


class Relationship:
    """A relationship between two entities."""

    def __init__(
        self,
        entities: List[Union[Node, Subgraph]],
        *,
        style: str = "SOLID",
        input_arrow: Optional[str] = None,
        output_arrow: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """Initialize a relationship.

        Args:
            entities: The entities to connect.
            style: The style of the relationship.
            input_arrow: The input arrow, valid values are "<", "o", "x"
            output_arrow: The output arrow, valid values are ">", "o", "x"
            label: The label of the relationship.
        """
        self.entities = entities
        self.style = style
        self.input_arrow = input_arrow
        self.output_arrow = output_arrow
        self.label = label

        if len(self.entities) != 2:
            raise ValueError("A relationship must have exactly two nodes.")

    def __str__(self) -> str:
        """Generate a relationship string."""
        output_string = ""
        output_string += self.entities[0]._internal_id
        if self.input_arrow:
            output_string += self.input_arrow
        output_string += RelationshipStyles[self.style].value
        if self.output_arrow:
            output_string += self.output_arrow
        if self.label:
            output_string += f"|{self.label}|"
        output_string += self.entities[1]._internal_id

        return output_string


class Flowchart(MermaidBase):
    """Base class for a flowchart."""

    def __init__(
        self,
        nodes: Optional[List[Node]] = None,
        relationships: Optional[List[Relationship]] = None,
        subgraphs: Optional[List[Subgraph]] = None,
        orientation: str = Orientation.TB.value,
        title: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize a flowchart.

        Args:
            nodes: A list of nodes in the flowchart.
            relationships: A list of relationships between entities in the flowchart.
            orientation: The orientation of the flowchart, defaults to "TB".
            title: The title of the flowchart.

        """
        super(Flowchart, self).__init__(**kwargs)
        self.nodes = nodes or []
        self.relationships = relationships or []
        self.subgraphs = subgraphs or []
        self.orientation = orientation
        self.title = title
        self.config = {}  # type: ignore

        self.set_internal_ids()

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
        """Create a relationship between two entities.

        Args:
            *args: Positional arguments to pass to the Relationship constructor.
            **kwargs: Keyword arguments to pass to the Relationship constructor.

        Returns:
            The created relationship.

        """
        relationship = Relationship(*args, **kwargs)
        self.add_relationships([relationship])
        return relationship

    def create_subgraph(self, *args: Any, **kwargs: Any) -> Subgraph:
        """Create a subgraph.

        Args:
            *args: Positional arguments to pass to the Subgraph constructor.
            **kwargs: Keyword arguments to pass to the Subgraph constructor.

        Returns:
            The created subgraph.

        """
        subgraph = Subgraph(*args, **kwargs)
        for existing_subgraph in self.subgraphs:
            for entity in subgraph.entities:
                if entity in existing_subgraph.entities:
                    raise ValueError(
                        "Cannot add a subgraph with entities that are already in another subgraph."
                    )
        self.add_subgraphs([subgraph])
        return subgraph

    def add_nodes(self, nodes: List[Node]) -> None:
        """Add a list of entities to the flowchart.

        Args:
            nodes: A list of entities to add to the flowchart.
        """
        for node in nodes:
            self.nodes.append(node)
        self.set_internal_ids()

    def add_relationships(self, relationships: List[Relationship]) -> None:
        """Add many relationships.

        Args:
            relationships: Relationships between the two entities.

        """
        for relationship in relationships:
            for node in relationship.entities:
                if node not in self.nodes:
                    raise ValueError(
                        "Relationships must be between entities in the flowchart."
                    )

        self.relationships += relationships

    def add_subgraphs(self, subgraphs: List[Subgraph]) -> None:
        """Add many subgraphs.

        Args:
            subgraphs: Subgraphs to add to the flowchart.

        """
        self.subgraphs += subgraphs
        self.set_internal_ids()

    def set_internal_ids(self) -> None:
        """Set the internal IDs of the entities."""
        ids = generate_internal_ids(len(self.nodes) + len(self.subgraphs))
        entities = self.nodes + self.subgraphs
        for entity, entity_id in zip(entities, ids):
            entity._internal_id = entity_id

    def get_flowchart_string(self) -> str:
        """Generate a flowchart string."""
        output_string = init_string(self.base_config, self.config)
        if self.title:
            output_string += f"---\ntitle: {self.title}\n---\n"
        output_string += f"graph {self.orientation}\n"

        # Remove nodes/subgraphs that are in subgraphs
        entities = self.nodes + self.subgraphs
        for subgraph in self.subgraphs:
            for entity in subgraph.entities:
                if entity in entities:
                    entities.remove(entity)
        for entity in entities:
            output_string += f"    {entity}\n"

        output_string += "\n"

        for relationship in self.relationships:
            output_string += f"    {relationship}\n"

        return output_string

    def __str__(self) -> str:
        return self.get_flowchart_string()
