import tempfile
from pathlib import Path

from barnacleboy.mermaid.gitgraph import GitGraph


def test_commit():
    git = GitGraph(theme="dark")
    git.commit(id="ZERO")

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        git.save(temp_file.name)

        assert Path(temp_file.name).exists()


def test_branch():
    git = GitGraph()
    git.branch("develop")

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        git.save(temp_file.name)

        assert Path(temp_file.name).exists()


def test_checkout():
    git = GitGraph()
    git.branch("develop")
    git.checkout("develop")

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        git.save(temp_file.name)

        assert Path(temp_file.name).exists()


def test_merge():
    git = GitGraph()
    git.commit()
    git.branch("develop")
    git.commit()
    git.checkout("main")
    git.merge("develop")

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        git.save(temp_file.name)

        assert Path(temp_file.name).exists()


def test_cherry_pick():
    git = GitGraph(
        theme="base",
        show_branches=True,
        show_commit_label=True,
        rotate_commit_label=True,
        main_branch_name="main",
        main_branch_order=0,
    )
    git.commit(id="ZERO")
    git.branch("develop")
    git.commit(id="A")
    git.commit(id="B")
    git.checkout("main")
    git.cherry_pick("A")

    with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_file:
        git.save(temp_file.name)

        assert Path(temp_file.name).exists()
