import tempfile
from pathlib import Path

from barnacleboy.mermaid.er_diagram import (
    EntityRelationDiagram,
    RelationshipType,
    Field,
)


def test_entity_relation_diagram():
    """Test the entity relation diagram class."""
    er_diagram = EntityRelationDiagram(theme="forest")
    er_diagram.add_entity(
        "Person",
        [Field("string", "name", "test", primary_key=True), Field("int", "age")],
    )
    er_diagram.add_entity(
        "Car", [Field("string", "make"), Field("string", "person_id", foreign_key=True)]
    )
    er_diagram.add_relationship(
        er_diagram.entities[0],
        er_diagram.entities[1],
        RelationshipType.ONE,
        RelationshipType.ZERO_OR_MORE,
        "owns",
    )

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        er_diagram.save(temp_file.name)

        assert Path(temp_file.name).exists()
