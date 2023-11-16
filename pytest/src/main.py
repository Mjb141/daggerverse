import dagger
from dagger.mod import function, object_type, field

BASE_PIP_COMMAND: list[str] = ["pip3", "install", "-r"]


def build_requirements_pip_commands(
    dependencies_files: str, pip_args: str | None
) -> list[list[str]]:
    additional_pip_args = [pip_args] if pip_args is not None else []

    return [
        BASE_PIP_COMMAND + [dependency_file] + additional_pip_args
        for dependency_file in dependencies_files.split(",")
    ]


@object_type
class PytestMod:
    """This is a Pytest class in a module"""

    is_pip: bool = False
    dependency_commands: list[list[str]] | None = None

    def container(self) -> dagger.Container:
        entrypoint = ["pytest"] if self.is_pip else ["poetry", "run"]

        return (
            dagger.container()
            .from_("mikebrown008/cgr-poetry:0.1.4")
            .with_workdir("/src")
            .with_user("root")
            .with_entrypoint(entrypoint)
        )

    @function
    async def with_poetry(self) -> "PytestMod":
        self.dependency_commands = [["poetry", "install"]]
        return self

    @function
    async def with_pip(self, requirements_files: str) -> "PytestMod":
        self.is_pip = True
        self.dependency_commands = build_requirements_pip_commands(
            requirements_files, None
        )
        return self

    @function
    async def test(self, src_dir: dagger.Directory, tests_dir: str) -> str:
        self.dependency_commands = (
            [["poetry", "install"]]
            if self.dependency_commands is None
            else self.dependency_commands
        )

        container = self.container().with_mounted_directory("/src", src_dir)

        for dependency_command in self.dependency_commands:
            container = container.with_exec(dependency_command)

        return await container.with_exec(["pytest", tests_dir]).stdout()
