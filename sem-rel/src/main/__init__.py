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
import json
from dagger import dag, function, object_type

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


def construct_cmd(check_if_ci: bool, dry_run: bool) -> list[str]:
    cmd = ["semantic-release"]
    cmd = cmd + ["--ci"] if check_if_ci else ["--no-ci"]
    cmd = cmd + ["--dry-run"] if dry_run else [""]
    return list(map(str.strip, cmd))


@object_type
class SemRel:
    @function
    async def release(
        self,
        dir: dagger.Directory,
        provider: str,
        token: dagger.Secret,
        check_if_ci: bool = True,
        dry_run: bool = True,
        add_branch: bool = False,
    ) -> dagger.Container:
        """Returns a container that runs semantic-release on your branch."""

        ctr = (
            dag.container()
            .from_("hoppr/semantic-release")
            .with_directory("/src", dir)
            .with_workdir("/src")
        )

        if add_branch:
            branch = await ctr.with_exec(["git", "branch", "--show-current"]).stdout()
            print(f"Current Branch: {branch}")

            rc_file = await dir.file(".releaserc.json").contents()
            print(f"Current '.releaserc.json':({type(rc_file)})\n {rc_file}")

            content = json.loads(rc_file)
            if "release" in content:
                content["release"]["branches"] = {"name": branch.strip()}
            elif "branches" in content:
                content["branches"] = {"name": branch.strip()}
            else:
                raise Exception(
                    "Neither 'release' nor 'branches' found at top-level in '.releaserc.json'"
                )

            dir = dir.without_file(".releaserc.json").with_new_file(
                ".releaserc.json", json.dumps(content)
            )

        env_var_key = "GH_TOKEN" if provider == "github" else "GL_TOKEN"

        return (
            dag.container()
            .from_("hoppr/semantic-release")
            .with_secret_variable(env_var_key, token)
            .with_directory("/src", dir)
            .with_workdir("/src")
            .with_exec(construct_cmd(check_if_ci, dry_run))
        )
