import dataclasses
from enum import Enum
from typing import Any, List, Tuple, Optional

from barnacleboy.mermaid.base import MermaidBase
from barnacleboy.mermaid.utils import init_string


class RelationshipType(Enum):
    """The type of relationship between two entities."""

    ZERO_OR_ONE: Tuple[str, str] = ("|o", "o|")
    ONE: Tuple[str, str] = ("||", "||")
    ZERO_OR_MORE: Tuple[str, str] = ("}o", "o{")
    ONE_OR_MORE: Tuple[str, str] = ("}|", "|{")


class Field:
    """An entity attribute."""

    def __init__(
        self,
        vartype: str,
        name: str,
        description: Optional[str] = None,
        primary_key: bool = False,
        foreign_key: bool = False,
    ) -> None:
        """Initialize an entity attribute.

        Args:
            vartype: The type of the attribute.
            name: The name of the attribute.
            description: The description of the attribute.
            primary_key: Whether the attribute is a primary key.
            foreign_key: Whether the attribute is a foreign key.
        """
        if primary_key and foreign_key:
            raise ValueError(
                "An attribute cannot be both a primary key and a foreign key."
            )

        self.vartype = vartype
        self.name = name
        self.description = description
        self.primary_key = primary_key
        self.foreign_key = foreign_key

    def __str__(self) -> str:
        """Get a string representation of the object."""
        output_string = f"  {self.vartype} {self.name}"
        if self.primary_key:
            output_string += " PK"
        if self.foreign_key:
            output_string += " FK"
        if self.description:
            output_string += f' "{self.description}"'
        return output_string


@dataclasses.dataclass
class Entity:
    """An entity in an ER diagram."""

    name: str
    attributes: Optional[List[Field]] = None

    def __str__(self) -> str:
        """Get a string representation of the object."""
        if not self.attributes:
            return self.name

        output_string = self.name + " {\n"
        for attribute in self.attributes:
            output_string += f"{attribute}\n"
        output_string += "}\n"
        return output_string


class Relationship:
    def __init__(
        self,
        entity1: Entity,
        entity2: Entity,
        relationship_1: RelationshipType,
        relationship_2: RelationshipType,
        label: str,
    ):
        """Initialize a relationship between two entities."""
        self.entity1 = entity1
        self.entity2 = entity2
        self.relationship_1 = relationship_1.value[0]
        self.relationship_2 = relationship_2.value[1]
        self.label = label

    def __str__(self) -> str:
        """Get a string representation of the object."""
        return f"{self.entity1.name}{self.relationship_1}--{self.relationship_2}{self.entity2.name} : {self.label}"


class EntityRelationDiagram(MermaidBase):
    """An entity relation diagram."""

    def __init__(
        self,
        entities: Optional[List[Entity]] = None,
        relationships: Optional[List[Relationship]] = None,
        **kwargs: Any,
    ):
        """Initialize an entity relationship diagram.

        Args:
            entities: A list of entities to add to the diagram.
            relationships: A list of relationships to add to the diagram.
            **kwargs: Keyword arguments to pass to the MermaidBase constructor.
        """
        super(EntityRelationDiagram, self).__init__(**kwargs)
        self.entities = entities if entities else []
        self.relationships = relationships if relationships else []
        self.config = {}

    def add_entity(self, *args: Any, **kwargs: Any) -> None:
        """Add an entity to the diagram.

        Args:
            *args: Positional arguments to pass to the Entity constructor.
            **kwargs: Keyword arguments to pass to the Entity constructor.
        """
        self.entities.append(Entity(*args, **kwargs))

    def add_relationship(self, *args: Any, **kwargs: Any) -> None:
        """Add a relationship to the diagram.

        Args:
            *args: Positional arguments to pass to the Relationship constructor.
            **kwargs: Keyword arguments to pass to the Relationship constructor.
        """
        self.relationships.append(Relationship(*args, **kwargs))

    def __str__(self) -> str:
        """Get a string representation of the object."""
        output_string = init_string(self.base_config, self.config)
        output_string += "erDiagram\n"
        for entity in self.entities:
            output_string += f"{entity}\n"
        for relationship in self.relationships:
            output_string += f"{relationship}\n"
        return output_string
