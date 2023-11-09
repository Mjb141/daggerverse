from typing import Annotated
import dagger
from dagger.mod import function

ANNOTATION_SRC_DIR = "The source directory, relative to your current directory"
ANNOTATION_TESTS_DIR = "The tests directory, relative to the 'src-dir'"
ANNOTATION_REQUIREMENTS_FILES = (
    "A comma-separated list of requirements files, relative to the 'tests-dir'"
)
ANNOTATION_PIP_ARGS = "Additional arguments to pass to the 'pip3 install' commands"

BASE_PIP_COMMAND: list[str] = ["pip3", "install", "-r"]


def build_requirements_pip_commands(
    dependencies_files: str, pip_args: str | None
) -> list[list[str]]:
    additional_pip_args = [pip_args] if pip_args is not None else []

    return [
        BASE_PIP_COMMAND + [dependency_file] + additional_pip_args
        for dependency_file in dependencies_files.split(",")
    ]


@function
async def pytest_with_pip(
    src_dir: Annotated[dagger.Directory, ANNOTATION_SRC_DIR],
    tests_dir: Annotated[str, ANNOTATION_TESTS_DIR],
    requirements_files: Annotated[str, ANNOTATION_REQUIREMENTS_FILES],
    pip_args: Annotated[str | None, ANNOTATION_PIP_ARGS] = None,
) -> str:
    container = (
        dagger.container()
        .from_("python:3.12-slim")
        .with_mounted_directory("/src", src_dir)
        .with_workdir("/src")
    )

    dependency_file_pip_commands = build_requirements_pip_commands(
        requirements_files, pip_args
    )

    for pip_command in dependency_file_pip_commands:
        container = container.with_exec(pip_command)

    return await container.with_exec(["pytest", tests_dir]).stdout()


@function
async def pytest_with_poetry(
    src_dir: Annotated[dagger.Directory, ANNOTATION_SRC_DIR],
    tests_dir: Annotated[str, ANNOTATION_TESTS_DIR],
) -> str:
    return (
        await dagger.container()
        .from_("mikebrown008/cgr-poetry:0.1.4")
        .with_mounted_directory("/src", src_dir)
        .with_workdir("/src")
        .with_user("root")
        .with_exec(["poetry", "install"], skip_entrypoint=True)
        .with_exec(["poetry", "run", "pytest", "-v", tests_dir], skip_entrypoint=True)
        .stdout()
    )
