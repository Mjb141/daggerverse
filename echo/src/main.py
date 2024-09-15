import dagger
from dagger import dag, function, object_type


@object_type
class EchoMod:
    """This module will just echo a value from another module"""

    secret: dagger.Secret | None = None

    def container(self) -> dagger.Container:
        return dag.container().from_("alpine:latest")

    @function
    async def with_secret(
        self,
        auth_id: dagger.Secret,
        auth_secret: dagger.Secret,
        secret_name: str,
        project_id: str,
        env: str,
        secret_path: str = "/",
    ) -> "EchoMod":
        """Fetch a secret from Infisical"""
        inf_secret = (
            dag.infisical()
            .with_universal_auth(auth_id, auth_secret)
            .get_secret_by_name(
                project_id=project_id,
                environment_slug=env,
                secret_path=secret_path,
                secret_name=secret_name,
            )
        )
        print(await inf_secret.plaintext())
        self.secret = inf_secret
        return self

    @function
    async def echo(self, word: str = "Hello") -> dagger.Container:
        """Echo a provided 'word' or a secret fetched prior"""
        if self.secret is None:
            return self.container().with_exec(["echo", f"Here's a word... {word}"])

        return self.container().with_exec(
            ["echo", f"Here's a secret! {await self.secret.plaintext()}"]
        )
