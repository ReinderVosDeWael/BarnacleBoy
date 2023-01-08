from barnacleboy.mermaid.entity_relation_diagram import (
    EntityRelationDiagram,
    RelationshipType,
)


def test_entity_relation_diagram():
    """Test the entity relation diagram class."""
    entity_relation_diagram = EntityRelationDiagram()
    entity_relation_diagram.add_entity("Person", [("string", "name"), ("int", "age")])
    entity_relation_diagram.add_entity("Car", [("string", "make"), ("string", "model")])
    entity_relation_diagram.add_relationship(
        entity_relation_diagram.entities[0],
        entity_relation_diagram.entities[1],
        RelationshipType.ONE,
        RelationshipType.ZERO_OR_MORE,
        "owns",
    )

    assert (
        str(entity_relation_diagram)
        == "erDiagram\nPerson {\n  string name\n  int age\n}\n\nCar {\n  string make\n  string model\n}\n\nPerson||--o{Car : owns\n"
    )
