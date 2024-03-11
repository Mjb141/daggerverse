import dagger
from dagger import dag, function, object_type, Doc
from typing import Annotated

from constants import *


@object_type
class Lambda:
    """Nodejs and Python Lambda ZIP file builder"""

    sdk: Annotated[str | None, Doc("Which SDK is in use: 'python' or 'node'")] = None
    source_dir: Annotated[
        dagger.Directory | None,
        Doc(
            "The module's source directory: location of 'pyproject.toml' or 'package.json'"
        ),
    ] = None

    aws_access_key_id: Annotated[dagger.Secret | None, Doc("AWS_ACCESS_KEY_ID")] = None
    aws_secret_access_key: Annotated[
        dagger.Secret | None, Doc("AWS_SECRET_ACCESS_KEY")
    ] = None
    aws_session_token: Annotated[dagger.Secret | None, Doc("AWS_SESSION_TOKEN")] = None
    region: Annotated[str | None, Doc("AWS_REGION")] = None
    account: Annotated[str | None, Doc("The AWS Account ID")] = None

    def container(self) -> dagger.Container:
        if self.source_dir is None:
            raise Exception(ERROR_MISSING_SOURCE_DIR)

        return (
            dag.container()
            .from_("mikebrown008/build-base:0.2.1")
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
    ) -> "Lambda":
        """Set AWS credentials for operations that require them."""
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.aws_session_token = ses_token
        self.region = region
        return self

    @function
    def with_sdk(self, sdk: str) -> "Lambda":
        """Set the SDK: 'node' or 'python'."""
        if sdk not in ["python", "node"]:
            raise Exception(ERROR_INCOMPATIBLE_SDK)

        self.sdk = sdk
        return self

    @function
    def with_source(self, source: dagger.Directory) -> "Lambda":
        """Provide a source directory relative to current directory"""
        self.source_dir = source
        return self

    @function
    def build(self) -> dagger.Container:
        """Build the package and it's dependencies"""
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
        """Export the built ZIP file"""
        return self.build().with_workdir("..").file(PACKAGE_FILE_NAME)

    @function
    def publish(self, bucket_name: str, object_key: str) -> dagger.Container:
        """Publish the built ZIP file to Amazon S3. Requires AWS Credentials."""
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
