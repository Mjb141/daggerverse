import dagger
from dagger import dag, function, object_type

PACKAGE_INSTALL_LOCATION = "dist"
PACKAGE_FILE_NAME = "lambda.zip"

COMMANDS_INSTALL_DEPENDENCIES = {
    "python": ["poetry", "install"],
    "node": ["npm", "install"],
}

COMMANDS_INSTALL_PACKAGE = {
    "python": [
        "poetry",
        "run",
        "pip",
        "install",
        "-t",
        PACKAGE_INSTALL_LOCATION,
        ".",
    ],
    "node": [
        "npx",
        "esbuild",
        "--bundle",
        "--minify",
        "--keep-names",
        "--sourcemap",
        "--sources-content=false",
        "--target=node20",
        "--platform=node",
        f"--outfile={PACKAGE_INSTALL_LOCATION}/index.js",
        "src/index.ts",
    ],
}

COMMANDS_ZIP_PACKAGE = {
    "python": ["zip", "-x", "'*.pyc'", "-r", f"../{PACKAGE_FILE_NAME}", "."],
    "node": ["zip", "-r", f"../{PACKAGE_FILE_NAME}", "."],
}

COMMAND_COPY_ZIP = ["aws", "s3", "cp", PACKAGE_FILE_NAME]

ERROR_MISSING_SOURCE_DIR = (
    "You must set a source directory using 'with-source --source <dir>'"
)
ERROR_MISSING_AWS_CREDENTIALS = "You must set AWS credentials with 'with-credentials'"
ERROR_INCOMPATIBLE_SDK = "You must choose either the 'python' or 'node' SDK"


@object_type
class LambdaMod:
    """Lambda module"""

    sdk: str | None = None
    source_dir: dagger.Directory | None = None

    aws_access_key_id: dagger.Secret | None = None
    aws_secret_access_key: dagger.Secret | None = None
    aws_session_token: dagger.Secret | None = None
    account: str | None = None
    region: str | None = None

    def container(self) -> dagger.Container:
        if self.source_dir is None:
            raise Exception(ERROR_MISSING_SOURCE_DIR)

        return (
            dag.container()
            .from_("mikebrown008/build-base:0.1")
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
    def with_sdk(self, sdk: str) -> "LambdaMod":
        if sdk not in ["python", "node"]:
            raise Exception(ERROR_INCOMPATIBLE_SDK)

        self.sdk = sdk
        return self

    @function
    def with_source(self, source: dagger.Directory) -> "LambdaMod":
        """Provide a source directory relative to current directory"""
        self.source_dir = source
        return self

    @function
    def build(self) -> dagger.Container:
        if self.sdk is None:
            raise Exception(ERROR_INCOMPATIBLE_SDK)

        print(f"Building a {self.sdk} package")
        return (
            self.container()
            .with_exec(COMMANDS_INSTALL_DEPENDENCIES[self.sdk], skip_entrypoint=True)
            .with_exec(COMMANDS_INSTALL_PACKAGE[self.sdk], skip_entrypoint=True)
            .with_workdir(PACKAGE_INSTALL_LOCATION)
            .with_exec(COMMANDS_ZIP_PACKAGE[self.sdk], skip_entrypoint=True)
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
