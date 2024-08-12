"""A generated module for SemRel functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

import dagger
from datetime import datetime
from dagger import dag, function, object_type, Doc
from typing import Annotated

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


def construct_cmd(check_if_ci: bool, dry_run: bool, branch: str | None = None):
    cmd = ["semantic-release"]
    if branch:
        cmd = cmd + [f"--branches {branch}"]

    if not check_if_ci:
        cmd = cmd + ["--no-ci"]

    if dry_run:
        cmd = cmd + ["--dry-run"]
    return cmd


@object_type
class SemRel:
    branch: str | None = None

    @function
    async def with_config(
        self,
        branch: Annotated[
            str | None,
            Doc("[Optional] The branch you want to add to the release configuration."),
        ] = None,
    ) -> "SemRel":
        """Modify the Semantic Release config file (.releaserc.json) for testing purposes."""
        if branch:
            print(f"Adding {branch.strip()} to branches CLI argument")
            self.branch = branch.strip()

        return self

    @function
    async def release(
        self,
        dir: dagger.Directory,
        provider: str,
        token: dagger.Secret,
        check_if_ci: bool = False,
        dry_run: bool = True,
    ) -> dagger.Container:
        """Returns a container that runs semantic-release on your branch."""
        env_var_key = "GH_TOKEN" if provider == "github" else "GL_TOKEN"

        cmd = construct_cmd(check_if_ci, dry_run, self.branch)
        print(f"Executing Semantic Release with command:\n{cmd}")

        return (
            dag.container()
            .from_("hoppr/semantic-release")
            .with_env_variable("TIME", datetime.now().strftime("%H%M%S"))
            .with_secret_variable(env_var_key, token)
            .with_directory("/src", dir)
            .with_workdir("/src")
            .with_exec(cmd)
        )
