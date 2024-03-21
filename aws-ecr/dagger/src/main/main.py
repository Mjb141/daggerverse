import dagger
from dagger import dag, function, object_type, Doc
from typing import Annotated


@object_type
class AwsEcr:
    access_key: Annotated[dagger.Secret | None, Doc("AWS_ACCESS_KEY_ID")] = None
    secret_key: Annotated[dagger.Secret | None, Doc("AWS_SECRET_ACCESS_KEY")] = None
    session_token: Annotated[dagger.Secret | None, Doc("AWS_SESSION_TOKEN")] = None
    region: Annotated[str, Doc("AWS_REGION")] = "eu-west-1"

    def cli(self) -> dagger.Container:
        if self.access_key is None or self.secret_key is None:
            raise Exception(
                "You must provide at least --access-key and --secret-key, and optionally --session-token"
            )

        ctr = (
            dag.container()
            .from_("public.ecr.aws/aws-cli/aws-cli:latest")
            .with_env_variable("AWS_REGION", self.region)
            .with_secret_variable("AWS_ACCESS_KEY_ID", self.access_key)
            .with_secret_variable("AWS_SECRET_ACCESS_KEY", self.secret_key)
        )

        if self.session_token is not None:
            ctr = ctr.with_secret_variable("AWS_SESSION_TOKEN", self.session_token)

        return ctr

    @function
    async def with_credentials(
        self,
        access_key: dagger.Secret | None = None,
        secret_key: dagger.Secret | None = None,
        session_token: dagger.Secret | None = None,
        region: str = "eu-west-1",
    ) -> "AwsEcr":
        """(Required for: push) Set AWS credentials"""
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.region = region
        return self

    @function
    async def push(
        self,
        ctr: dagger.Container,
        account_id: str,
        repository: str,
        tags: list[str] | None = None,
    ) -> list[str]:
        """Push an Image to AWS ECR"""
        password = dag.set_secret(
            "aws-reg-cred",
            await self.cli()
            .with_exec(["--region", self.region, "ecr", "get-login-password"])
            .stdout(),
        )

        base = f"{account_id}.dkr.ecr.{self.region}.amazonaws.com"

        if tags is None:
            return [
                await ctr.with_registry_auth(base, "AWS", password).publish(
                    f"{base}/{repository}"
                )
            ]

        publish_targets = [f"{base}/{repository}:{tag}" for tag in tags]

        return [
            await ctr.with_registry_auth(
                f"{account_id}.dkr.ecr.{self.region}.amazonaws.com", "AWS", password
            ).publish(target)
            for target in publish_targets
        ]
