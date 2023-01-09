import dataclasses
from typing import Optional, List, Union, Any

from barnacleboy.mermaid.base import MermaidBase
from barnacleboy.mermaid.utils import init_string

VALID_COMMIT_TYPES = {"NORMAL", "REVERSE", "HIGHLIGHT"}
VALID_THEMES = {"base", "forest", "dark", "default", "neutral"}


@dataclasses.dataclass
class MergeCommit:
    """Superclass for a merge or commit in a git graph."""

    id: Optional[str] = None
    type: Optional[str] = None
    tag: Optional[str] = None

    def __str__(self) -> str:
        """Get a string representation of the object."""
        output_string = type(self).__name__.lower()
        for attribute, value in dataclasses.asdict(self).items():
            if value:
                output_string += f' {attribute}: "{value}"'

        return output_string


class Merge(MergeCommit):
    """A merge commit in a git graph."""

    def __init__(
        self,
        branch_name: str,
        id: Optional[str] = None,
        commit_type: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> None:
        """Initialize a merge commit.

        Args:
            branch_name: The name of the branch to merge.
            id: The id of the commit.
            commit_type: The type of the commit.
            tag: The tag of the commit.
        """
        super().__init__(id, commit_type, tag)
        self.branch_name = branch_name

    def __str__(self) -> str:
        """Get a string representation of the object."""
        output_string = super().__str__()
        return output_string.replace("merge", f"merge {self.branch_name}")


class Commit(MergeCommit):
    """A commit in a git graph."""

    pass


@dataclasses.dataclass
class Branch:
    """Dataclass for a branch in the git graph.

    Args:
        name: The name of the branch.
    """

    name: str

    def __str__(self) -> str:
        """Get a string representation of the object."""
        return f"branch {self.name}"


class GitGraph(MermaidBase):
    """A git graph model."""

    def __init__(
        self,
        *,
        show_branches: bool = True,
        show_commit_label: bool = True,
        rotate_commit_label: bool = True,
        main_branch_name: str = "main",
        main_branch_order: int = 0,
        **kwargs: Any,
    ) -> None:
        """Create a git graph.

        Args:
            show_branches: Whether to show branches.
            show_commit_label: Whether to show commit labels.
            rotate_commit_label: Whether to rotate commit labels.
            main_branch_name: The name of the main branch.
            main_branch_order: The order of the main branch.
            kwargs: The kwargs to pass to the MermaidBase class.
        """
        super(GitGraph, self).__init__(**kwargs)
        self.log: List[Union[MergeCommit, Branch, str]] = []
        self.commits: List[Commit] = []
        self.branches = [Branch("main")]
        self.show_branches = show_branches
        self.show_commit_label = show_commit_label
        self.rotate_commit_label = rotate_commit_label
        self.main_branch_name = main_branch_name
        self.main_branch_order = main_branch_order
        self.config = {}  # type: ignore

    def commit(
        self,
        id: Optional[str] = None,
        commit_type: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> None:
        """Create a commit.

        Args:
            id: The id of the commit.
            commit_type: The type of the commit, can be "NORMAL", "REVERSE", or "HIGHLIGHT".
            tag: The tag of the commit.
        """
        if commit_type and commit_type not in VALID_COMMIT_TYPES:
            raise ValueError(f"Invalid commit type: {commit_type}")

        if id:
            for existing_commit in self.commits:
                if existing_commit.id == id:
                    raise ValueError(f"Commit {id} already exists")

        commit = Commit(id, commit_type, tag)
        self.commits.append(commit)
        self.log.append(str(commit))

    def branch(self, branch_name: str) -> None:
        """Create a new branch.

        Args:
            branch_name: The name of the branch to create.

        Raises:
            ValueError: If the branch already exists.
        """
        for existing_branch in self.branches:
            if existing_branch.name == branch_name:
                raise ValueError(f"Branch {branch_name} already exists")

        branch = Branch(branch_name)
        self.branches.append(branch)
        self.log.append(str(branch))

    def checkout(self, branch_name: str) -> None:
        """Checkout a branch.

        Args:
            branch_name: The name of the branch to checkout.

        Raises:
            ValueError: If the branch does not exist.
        """
        for existing_branch in self.branches:
            if existing_branch.name == branch_name:
                self.log.append(f"checkout {branch_name}")
                return
        raise ValueError(f"Branch {branch_name} does not exist")

    def merge(
        self,
        branch_name: str,
        id: Optional[str] = None,
        commit_type: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> None:
        """Merge a branch.

        Args:
            branch_name: The name of the branch to merge.
            id: The id of the merge commit.
            commit_type: The commit_type of the merge commit, can be "NORMAL", "REVERSE", or "HIGHLIGHT".
            tag: The tag of the merge commit.

        Raises:
            ValueError: If the branch does not exist.
        """
        if commit_type and commit_type not in VALID_COMMIT_TYPES:
            raise ValueError(f"Invalid commit type: {commit_type}")

        merge = Merge(branch_name, id, commit_type, tag)
        for branch in self.branches:
            if branch.name == branch_name:
                self.log.append(str(merge))
                return
        raise ValueError(f"Branch {branch_name} does not exist")

    def cherry_pick(self, commit_id: str) -> None:
        """Cherry-pick a commit.

        Args:
            commit_id: The id of the commit to cherry-pick.

        Raises:
            ValueError: If the commit does not exist.
        """

        for commit in self.commits:
            if commit.id == commit_id:
                self.log.append(f'cherry-pick id:"{commit_id}"')
                return
        raise ValueError(f"Commit {commit_id} does not exist")

    def __str__(self) -> str:
        """Get a string representation of the object."""
        output_string = init_string(self.base_config, self.config)
        output_string += "gitGraph\n"
        for line in self.log:
            output_string += f"{line}\n"
        return output_string
