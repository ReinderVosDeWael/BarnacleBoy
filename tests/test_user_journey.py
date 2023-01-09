from barnacleboy.mermaid.user_journey import Task, Section, UserJourney


def test_task():
    """Test the task class."""
    task = Task("Use the force", 5, ["Leia", "Luke"])

    assert task.description == "Use the force"
    assert task.rating == 5
    assert task.people == ["Leia", "Luke"]

    assert str(task) == "Use the force: 5: Leia, Luke"


def test_section():
    """Test the section class."""
    section = Section("Return of the Jedi")

    section.add_task("Use the force", 5, ["Leia", "Luke"])

    assert section.title == "Return of the Jedi"
    assert section.tasks[0] == Task("Use the force", 5, ["Leia", "Luke"])

    assert str(section) == "section Return of the Jedi\nUse the force: 5: Leia, Luke\n"


def test_user_journey():
    """Test the user journey class."""
    user_journey = UserJourney("Original Trilogy")

    user_journey.add_section("Return of the Jedi")
    user_journey.sections[0].add_task("Use the force", 5, ["Leia", "Luke"])

    assert user_journey.title == "Original Trilogy"

    assert (
        str(user_journey)
        == "%%{init: {'theme': 'base'}}%%\njourney\ntitle Original Trilogy\nsection Return of the Jedi\nUse the force: 5: Leia, Luke\n"
    )
