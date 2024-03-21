import dagger
from dagger import dag, function, object_type


@object_type
class TestEcr:
    @function
    async def test_build(
        self,
        dir: dagger.Directory,
        ak: dagger.Secret,
        sk: dagger.Secret,
        st: dagger.Secret,
        aid: str,
        repo: str,
    ) -> list[str]:
        image = dir.docker_build()
        return (
            await dag.aws_ecr()
            .with_credentials(access_key=ak, secret_key=sk, session_token=st)
            .push(image, aid, repo)
        )

    @function
    async def test_image(
        self,
        ak: dagger.Secret,
        sk: dagger.Secret,
        st: dagger.Secret,
        aid: str,
        repo: str,
    ) -> list[str]:
        image = dag.container().from_("alpine:latest")
        return (
            await dag.aws_ecr()
            .with_credentials(access_key=ak, secret_key=sk, session_token=st)
            .push(image, aid, repo)
        )

    @function
    async def test_tagging(
        self,
        ak: dagger.Secret,
        sk: dagger.Secret,
        st: dagger.Secret,
        aid: str,
        repo: str,
        tags: list[str],
    ) -> list[str]:
        image = dag.container().from_("alpine:latest")
        return (
            await dag.aws_ecr()
            .with_credentials(access_key=ak, secret_key=sk, session_token=st)
            .push(image, aid, repo, tags=tags)
        )
