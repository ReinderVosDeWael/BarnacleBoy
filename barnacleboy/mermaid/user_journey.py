""" Mermaid diagrams for User Journeys. """
import dataclasses
from typing import Optional, List

from barnacleboy.mermaid.base import MermaidBase


@dataclasses.dataclass
class Task:
    """A task in a user journey."""

    description: str
    rating: int
    people: List[str]

    def __str__(self) -> str:
        """Get a string representation of the object."""
        return f"{self.description}: {self.rating}: {', '.join(self.people)}"


class Section:
    """A section in a user journey."""

    def __init__(self, title: str, tasks: Optional[List[Task]] = None) -> None:
        """Initialize a section.

        Args:
            title: The title of the section.
            tasks: A list of tasks in the section.
        """
        self.title = title
        self.tasks = tasks if tasks else []

    def add_task(self, description: str, rating: int, people: list[str]) -> None:
        """Append a task to the section.

        Args:
            description: The description of the task.
            rating: The rating of the task.
            people: A list of people who are responsible for the task.
        """
        self.tasks.append(Task(description, rating, people))

    def get_section_string(self) -> str:
        """Get a string representation of the object."""
        output_string = f"section {self.title}\n"
        for task in self.tasks:
            output_string += f"{task}\n"
        return output_string

    def __str__(self) -> str:
        return self.get_section_string()


class UserJourney(MermaidBase):
    """A user journey model."""

    def __init__(self, title: str, sections: Optional[List[Section]] = None):
        """Initialize a user journey.

        Args:
            title: The title of the user journey.
            sections: A list of sections in the user journey.
        """
        self.title = title
        self.sections = sections if sections else []

    def add_section(self, title: str, tasks: Optional[List[Task]] = None) -> None:
        """Add a section to the user journey.

        Args:
            title: The title of the section.
            tasks: A list of tasks in the section.
        """
        self.sections.append(Section(title, tasks))

    def get_user_journey_string(self) -> str:
        """Get a string representation of the object."""
        output_string = "journey\n"
        output_string += f"title {self.title}\n"
        for section in self.sections:
            output_string += str(section)
        return output_string

    def __str__(self) -> str:
        return self.get_user_journey_string()
