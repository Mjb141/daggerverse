import dagger
from dagger import dag, function, object_type


@object_type
class Kics:
    @function
    def scan(self, dir: dagger.Directory) -> dagger.Container:
        return (
            dag.container()
            .from_("checkmarx/kics:latest")
            .with_directory("/src", dir)
            .with_workdir("/src")
            .with_exec(["scan", "-p", ".", "-o", "/src/", "--fail-on", "high"])
        )
