import dagger
from dagger import dag, function, object_type

BASE_PIP_COMMAND: list[str] = ["pip3", "install", "-r"]


def build_requirements_pip_commands(
    dependency_file: str, pip_args: str | None
) -> list[str]:
    additional_pip_args = [pip_args] if pip_args is not None else []
    return BASE_PIP_COMMAND + [dependency_file] + additional_pip_args


@object_type
class PytestMod:
    """This is a Pytest class in a module"""

    dependency_command: list[str] | None = None

    def container(self) -> dagger.Container:
        return (
            dag.container()
            .from_("mikebrown008/cgr-poetry:0.1.4")
            .with_workdir("/src")
            .with_user("root")
        )

    @function
    def with_poetry(self) -> "PytestMod":
        self.dependency_command = ["poetry", "install"]
        return self

    @function
    def with_pip(self, requirements_files: str) -> "PytestMod":
        self.dependency_command = build_requirements_pip_commands(
            requirements_files, None
        )
        return self

    @function
    async def test(self, src_dir: dagger.Directory, tests_dir: str) -> dagger.Container:
        if self.dependency_command is None:
            raise Exception(
                "You must use either 'with_pip' or 'with_poetry' before calling 'test'"
            )

        container = (
            self.container()
            .with_mounted_directory("/src", src_dir)
            .with_exec(self.dependency_command, skip_entrypoint=True)
        )

        return await container.with_exec(["pytest", tests_dir])
