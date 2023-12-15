import dagger
from dagger import dag, function, object_type

PACKAGE_INSTALL_LOCATION = "dist/lambda"
PACKAGE_FILE_NAME = "lambda.zip"

COMMAND_INSTALL_DEPENDENCIES = ["poetry", "install"]
COMMAND_INSTALL_PACKAGE = [
    "poetry",
    "run",
    "pip",
    "install",
    "-t",
    PACKAGE_INSTALL_LOCATION,
    ".",
]
COMMAND_ZIP_PACKAGE = ["zip", "-x", "'*.pyc'", "-r", f"../{PACKAGE_FILE_NAME}", "."]
COMMAND_COPY_ZIP = ["aws", "s3", "cp", PACKAGE_FILE_NAME]

ERROR_MISSING_SOURCE_DIR = (
    "You must set a source directory using 'with-source --source <dir>'"
)
ERROR_MISSING_AWS_CREDENTIALS = "You must set AWS credentials with 'with-credentials'"


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
            .from_("mikebrown008/cgr-poetry:0.2")
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
        if self.source_dir is None:
            raise Exception(ERROR_MISSING_SOURCE_DIR)

        return (
            self.container()
            .with_exec(COMMAND_INSTALL_DEPENDENCIES, skip_entrypoint=True)
            .with_exec(COMMAND_INSTALL_PACKAGE, skip_entrypoint=True)
            .with_workdir(PACKAGE_INSTALL_LOCATION)
            .with_exec(COMMAND_ZIP_PACKAGE, skip_entrypoint=True)
        )

    @function
    def export(self) -> dagger.File:
        return self.build().with_workdir("..").file(PACKAGE_FILE_NAME)

    @function
    def publish(self, bucket_name: str, object_key: str) -> dagger.Container:
        if self.aws_access_key_id is None:
            raise Exception(ERROR_MISSING_AWS_CREDENTIALS)
        if self.aws_secret_access_key is None:
            raise Exception(ERROR_MISSING_AWS_CREDENTIALS)
        if self.aws_session_token is None:
            raise Exception(ERROR_MISSING_AWS_CREDENTIALS)

        return (
            self.build()
            .with_secret_variable("AWS_ACCESS_KEY_ID", self.aws_access_key_id)
            .with_secret_variable("AWS_SECRET_ACCESS_KEY", self.aws_secret_access_key)
            .with_secret_variable("AWS_SESSION_TOKEN", self.aws_session_token)
            .with_workdir("..")
            .with_exec(
                COMMAND_COPY_ZIP + [f"s3://{bucket_name}/{object_key}"],
                skip_entrypoint=True,
            )
        )
