import dagger
from dagger import dag, function, object_type

BASE_PIP_COMMAND: list[str] = ["python", "-m", "pip", "install", "-r"]
CONFIG_NOT_PROVIDED_ERROR: str = (
    "You must use either 'with_pip' or 'with_poetry' before calling 'test'"
)


def build_requirements_pip_commands(
    dependency_file: str, pip_args: str | None
) -> list[str]:
    additional_pip_args = [pip_args] if pip_args is not None else []
    return BASE_PIP_COMMAND + [dependency_file] + additional_pip_args


@object_type
class PytestMod:
    """This is a Pytest class in a module"""

    dependency_command: list[str] | None = None
    run_command: list[str] | None = None
    entrypoint: list[str] | None = None

    def container(self) -> dagger.Container:
        if self.entrypoint is None:
            raise Exception(CONFIG_NOT_PROVIDED_ERROR)

        return (
            dag.container()
            .from_("mikebrown008/cgr-poetry:0.1.4")
            .with_workdir("/src")
            .with_user("root")
            .with_entrypoint(self.entrypoint)
        )

    @function
    def with_poetry(self) -> "PytestMod":
        self.entrypoint = ["poetry"]
        self.dependency_command = ["install"]
        self.run_command = ["run", "pytest"]
        return self

    @function
    def with_pip(self, requirement_file: str) -> "PytestMod":
        self.entrypoint = []
        self.dependency_command = build_requirements_pip_commands(
            requirement_file, None
        )
        self.run_command = ["pytest"]
        return self

    @function
    async def test(self, src_dir: dagger.Directory, tests_dir: str) -> dagger.Container:
        if self.dependency_command is None or self.run_command is None:
            raise Exception(CONFIG_NOT_PROVIDED_ERROR)

        return (
            self.container()
            .with_mounted_directory("/src", src_dir)
            .with_exec(self.dependency_command)
            .with_exec(self.run_command + [tests_dir])
        )
