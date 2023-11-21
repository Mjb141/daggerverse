import dagger
from dagger.mod import function, object_type


@object_type
class CdkMod:
    """CDK module"""

    aws_access_key_id: dagger.Secret | None = None
    aws_secret_access_key: dagger.Secret | None = None
    aws_session_token: dagger.Secret | None = None
    account: str | None = None
    region: str | None = None

    environment_variables: list[dict[str, str]] | None = None

    source_dir: dagger.Directory | None = None

    def container(self) -> dagger.Container:
        if self.source_dir is None:
            self.source_dir = dagger.host().directory(".")

        return (
            dagger.container()
            .from_("node:20.9.0-alpine3.18")
            .with_workdir("/src")
            .with_directory("/src", self.source_dir, exclude=["node_modules/**"])
        )

    @function
    def with_aws_credentials(
        self,
        access_key: dagger.Secret,
        secret_key: dagger.Secret,
        ses_token: dagger.Secret | None = None,
    ) -> "CdkMod":
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.aws_session_token = ses_token
        return self

    @function
    def with_aws_config(
        self,
        region: str,
        account: str,
    ) -> "CdkMod":
        """Provide an account number and an AWS region"""
        self.account = account
        self.region = region
        return self

    @function
    def with_env_var(self, key: str, value: str) -> "CdkMod":
        """Provide a single environment variable key and value.
        Can be provided multiple times"""
        if self.environment_variables is None:
            self.environment_variables = []

        self.environment_variables.append({key: value})
        return self

    @function
    def with_source(self, source: dagger.Directory) -> "CdkMod":
        """Provide a source directory relative to current directory"""
        self.source_dir = source
        return self

    @function
    def synth(self) -> dagger.Container:
        return (
            self.container()
            .with_exec(["npm", "ci"])
            .with_exec(["npm", "run", "cdk", "synth"])
        )

    @function
    def deploy(self) -> dagger.Container:
        return (
            self.container()
            .with_exec(["npm", "ci"])
            .with_exec(["npm", "run", "cdk", "deploy"])
        )
