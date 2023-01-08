import dataclasses
from enum import Enum
from typing import List, Tuple, Optional

from barnacleboy.mermaid.base import MermaidBase


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
    name: str
    attributes: Optional[List[Field]] = None

    def __str__(self) -> str:
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
        self.entity1 = entity1
        self.entity2 = entity2
        self.relationship_1 = relationship_1.value[0]
        self.relationship_2 = relationship_2.value[1]
        self.label = label

    def __str__(self) -> str:
        return f"{self.entity1.name}{self.relationship_1}--{self.relationship_2}{self.entity2.name} : {self.label}"


class EntityRelationDiagram(MermaidBase):
    def __init__(
        self,
        entities: Optional[List[Entity]] = None,
        relationships: Optional[List[Relationship]] = None,
    ):
        self.entities = entities if entities else []
        self.relationships = relationships if relationships else []

    def add_entity(self, *args, **kwargs):
        self.entities.append(Entity(*args, **kwargs))

    def add_relationship(self, *args, **kwargs):
        self.relationships.append(Relationship(*args, **kwargs))

    def __str__(self) -> str:
        output_string = "erDiagram\n"
        for entity in self.entities:
            output_string += f"{entity}\n"
        for relationship in self.relationships:
            output_string += f"{relationship}\n"
        return output_string
