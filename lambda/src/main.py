import dagger
from dagger import dag, function, object_type

INSTALL_DEPENDENCIES = ["poetry", "install"]
INSTALL_PACKAGE = ["poetry", "run", "pip", "install", "-t", "dist/lambda", "."]
ZIP_PACKAGE = ["zip", "-x", "'*.pyc'", "-r", "../lambda.zip", "."]


@object_type
class LambdaMod:
    """Lambda module"""

    aws_access_key_id: dagger.Secret | None = None
    aws_secret_access_key: dagger.Secret | None = None
    aws_session_token: dagger.Secret | None = None
    account: str | None = None
    region: str | None = None

    source_dir: dagger.Directory | None = None

    def container(self) -> dagger.Container:
        if self.source_dir is None:
            self.source_dir = dag.host().directory(".")

        return (
            dag.container()
            .from_("mikebrown008/cgr-poetry:0.1.5")
            .with_workdir("/src")
            .with_directory("/src", self.source_dir)
        )

    @function
    def with_credentials(
        self,
        access_key: dagger.Secret,
        secret_key: dagger.Secret,
        ses_token: dagger.Secret | None = None,
        region: str = "eu-west-1",
    ) -> "LambdaMod":
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.aws_session_token = ses_token
        self.region = region
        return self

    @function
    def with_source(self, source: dagger.Directory) -> "LambdaMod":
        """Provide a source directory relative to current directory"""
        self.source_dir = source
        return self

    @function
    def build(self) -> dagger.Container:
        if self.region is None:
            raise Exception("You must set a region using '--with-config'")

        return (
            self.container()
            .with_exec(INSTALL_DEPENDENCIES, skip_entrypoint=True)
            .with_exec(INSTALL_PACKAGE, skip_entrypoint=True)
            .with_workdir("dist/lambda/")
            .with_exec(ZIP_PACKAGE, skip_entrypoint=True)
        )

    @function
    def export(self) -> dagger.File:
        return self.build().with_workdir("..").file("lambda.zip")
