import dagger
from dagger import dag, function, object_type, Doc
from typing import Annotated


@object_type
class Kics:
    @function
    def scan(
        self,
        dir: Annotated[dagger.Directory, Doc("Directory to scan, relative to `pwd`")],
    ):
        """Scan a directory and contained subdirs with KICS default configuration."""
        return (
            dag.container()
            .from_("checkmarx/kics:latest")
            .with_directory("/src", dir)
            .with_exec(
                ["kics", "scan", "-p", "/src", "-o", "/src/", "--fail-on", "high"]
            )
        )
