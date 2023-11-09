from src.main import build_requirements_pip_commands


def test_single_requirements_file():
    dep_files = "reqs1.txt"
    commands = build_requirements_pip_commands(dep_files, None)
    assert commands == [["pip3", "install", "-r", "reqs1.txt"]]


def test_multiple_requirements_files():
    dep_files = "reqs1.txt,reqs2.txt"
    commands = build_requirements_pip_commands(dep_files, None)
    assert commands == [
        ["pip3", "install", "-r", "reqs1.txt"],
        ["pip3", "install", "-r", "reqs2.txt"],
    ]


def test_single_requirements_file_with_pip_arg():
    dep_files = "reqs1.txt"
    pip_args = "--no-compile"
    commands = build_requirements_pip_commands(dep_files, pip_args)
    assert commands == [["pip3", "install", "-r", "reqs1.txt", "--no-compile"]]


def test_multiple_requirements_file_with_pip_arg():
    dep_files = "reqs1.txt,reqs2.txt"
    pip_args = "--no-compile"
    commands = build_requirements_pip_commands(dep_files, pip_args)
    assert commands == [
        ["pip3", "install", "-r", "reqs1.txt", "--no-compile"],
        ["pip3", "install", "-r", "reqs2.txt", "--no-compile"],
    ]
