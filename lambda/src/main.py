import dagger
from dagger import dag, function, object_type

INSTALL_PACKAGE = ["poetry", "run", "pip", "install", "-t", "dist/lambda", "."]
MOVE_DIR = ["cd", "dist/lambda"]
ZIP_PACKAGE = ["zip", "-x", "'*.pyc'", "-r", "../lambda.zip"]


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
            .from_("mikebrown008/cgr-poetry:0.1.4")
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
    def publish(self) -> dagger.Container:
        if self.region is None:
            raise Exception("You must set a region using '--with-config'")
        if self.aws_access_key_id is None:
            raise Exception("You must set AWS credentials with '--with-credentials'")
        if self.aws_secret_access_key is None:
            raise Exception("You must set AWS credentials with '--with-credentials'")
        if self.aws_session_token is None:
            raise Exception("You must set AWS credentials with '--with-credentials'")

        container = (
            self.container()
            .with_secret_variable("AWS_ACCESS_KEY_ID", self.aws_access_key_id)
            .with_secret_variable("AWS_SECRET_ACCESS_KEY", self.aws_secret_access_key)
            .with_secret_variable("AWS_SESSION_TOKEN", self.aws_session_token)
            .with_env_variable("AWS_REGION", self.region)
        )

        return (
            container.with_exec(INSTALL_PACKAGE)
            .with_exec(MOVE_DIR)
            .with_exec(ZIP_PACKAGE)
        )
