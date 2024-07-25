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
from dagger import dag, function, object_type

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


@object_type
class SemRel:
    @function
    def release(
        self,
        dir: dagger.Directory,
        token: dagger.Secret,
        check_if_ci: bool = True,
        dry_run: bool = True,
    ) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return (
            dag.container()
            .from_("hoppr/semantic-release")
            .with_secret_variable("GH_TOKEN", token)
            .with_directory("/src", dir)
            .with_workdir("/src")
            .with_exec(["ls", "-la"])
            .with_exec(
                [
                    "semantic-release",
                    "--ci" if check_if_ci else "--no-ci",
                    "--dry-run" if not dry_run else "",
                ]
            )
        )
