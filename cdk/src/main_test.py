from typing import NamedTuple
import dagger
from dagger.mod import function, object_type


class CdkSecret(NamedTuple):
    key: str
    value: dagger.Secret


class CdkEnvVar(NamedTuple):
    key: str
    value: str


def container(
    source: dagger.Directory,
    secrets: list[CdkSecret],
    env_vars: list[CdkEnvVar],
) -> dagger.Container:
    base = (
        dagger.container()
        .from_("node:20.9.0-alpine3.18")
        .with_workdir("/src")
        .with_directory("/src", source, exclude=["node_modules/**"])
    )

    for secret in secrets:
        base = base.with_secret_variable(secret.key.upper(), secret.value)

    for env_var in env_vars:
        base = base.with_env_variable(env_var.key.upper(), env_var.value)

    return base


@object_type
class CdkMod:
    """CDK module"""

    aws_access_key_id: dagger.Secret | None = None
    aws_secret_access_key: dagger.Secret | None = None
    aws_session_token: dagger.Secret | None = None
    account: str | None = None
    region: str | None = None

    environment_variables: list[CdkEnvVar] | None = None

    source_dir: dagger.Directory | None = None

    @function
    def with_credentials(
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
    def with_config(
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

        self.environment_variables.append(CdkEnvVar(key, value))
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
        if self.account is None:
            raise Exception("You must set an account number using '--with-config'")
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
            .with_env_variable("AWS_ACCOUNT_ID", self.account)
        )

        if self.environment_variables is not None:
            for env_var_pair in self.environment_variables:
                container = container.with_env_variable(
                    env_var_pair[0], env_var_pair[1]
                )

        return container.with_exec(["npm", "ci"]).with_exec(
            ["npm", "run", "cdk", "deploy"]
        )
