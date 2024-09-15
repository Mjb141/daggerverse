import dagger
from dagger import dag, function, object_type


@object_type
class EchoMod:
    """This module will just echo a value from another module"""

    secret: dagger.Secret | None = None

    def container(self) -> dagger.Container:
        return dag.container().from_("alpine:latest")

    @function
    def with_secret(
        self,
        auth_id: dagger.Secret,
        auth_secret: dagger.Secret,
        secret_name: str,
        project_id: str,
        env: str,
    ) -> "EchoMod":
        """Fetch a secret from Infisical"""
        self.secret = dag.infisical(auth_id, auth_secret).get_secret(
            secret_name, project_id, env
        )
        return self

    @function
    async def echo(self, word: str = "Hello") -> dagger.Container:
        """Echo a provided 'word' or a secret fetched prior"""
        if self.secret is None:
            return self.container().with_exec(["echo", f"Here's a word... {word}"])

        return self.container().with_exec(
            ["echo", f"Here's a secret! {await self.secret.plaintext()}"]
        )
