import dagger
import dataclasses

from dagger import dag, function, object_type, Platform, BuildArg


@object_type
class Build:
    build_args: dict[str, str] = dataclasses.field(default_factory=dict)

    @function
    def with_build_arg(self, key: str, value: str) -> "Build":
        self.build_args[key] = value
        return self

    @function
    def build(
        self,
        dir: dagger.Directory,
        file_name: str = "Dockerfile",
        platform: str = "linux/amd64",
    ) -> dagger.Container:
        return dir.docker_build(
            platform=Platform(platform),
            dockerfile=file_name,
            build_args=[BuildArg(k, v) for (k, v) in self.build_args.items()],
        )
