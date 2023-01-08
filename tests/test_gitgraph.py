from barnacleboy.mermaid.gitgraph import GitGraph


def test_commit():
    git = GitGraph()
    git.commit(id="ZERO")

    assert (
        str(git)
        == "%%{'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': True, 'showCommitLabel': True, 'rotateCommitLabel': True, 'mainBranch': 'main', 'mainBranchOrder': 0}}%%\ngitGraph\ncommit id: \"ZERO\"\n"
    )


def test_branch():
    git = GitGraph()
    git.branch("develop")

    assert (
        str(git)
        == "%%{'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': True, 'showCommitLabel': True, 'rotateCommitLabel': True, 'mainBranch': 'main', 'mainBranchOrder': 0}}%%\ngitGraph\nbranch develop\n"
    )


def test_checkout():
    git = GitGraph()
    git.branch("develop")
    git.checkout("develop")

    assert (
        str(git)
        == "%%{'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': True, 'showCommitLabel': True, 'rotateCommitLabel': True, 'mainBranch': 'main', 'mainBranchOrder': 0}}%%\ngitGraph\nbranch develop\ncheckout develop\n"
    )


def test_merge():
    git = GitGraph()
    git.commit()
    git.branch("develop")
    git.commit()
    git.checkout("main")
    git.merge("develop")

    assert (
        str(git)
        == "%%{'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': True, 'showCommitLabel': True, 'rotateCommitLabel': True, 'mainBranch': 'main', 'mainBranchOrder': 0}}%%\ngitGraph\ncommit\nbranch develop\ncommit\ncheckout main\nmerge develop\n"
    )


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

    assert (
        str(git)
        == "%%{'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': True, 'showCommitLabel': True, 'rotateCommitLabel': True, 'mainBranch': 'main', 'mainBranchOrder': 0}}%%\ngitGraph\ncommit id: \"ZERO\"\nbranch develop\ncommit id: \"A\"\ncommit id: \"B\"\ncheckout main\ncherry-pick id:\"A\"\n"
    )
