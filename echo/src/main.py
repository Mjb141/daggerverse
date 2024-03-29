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
        name: str,
        token: dagger.Secret,
        env: str = "dev",
        path: str = "/",
    ) -> "EchoMod":
        """Fetch a secret from Infisical"""
        self.secret = dag.infisical().get_secret(name, token, env, path)
        return self

    @function
    async def echo(self, word: str = "Hello") -> dagger.Container:
        """Echo a provided 'word' or a secret fetched prior"""
        if self.secret is None:
            return self.container().with_exec(["echo", f"Here's a word... {word}"])

        return self.container().with_exec(
            ["echo", f"Here's a secret! {await self.secret.plaintext()}"]
        )
