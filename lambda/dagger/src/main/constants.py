PACKAGE_INSTALL_LOCATION = "dist"
PACKAGE_FILE_NAME = "lambda.zip"

COMMANDS_INSTALL_DEPENDENCIES = {
    "python": ["poetry", "install"],
    "node": ["npm", "install"],
}

COMMANDS_INSTALL_PACKAGE = {
    "python": [
        "poetry",
        "run",
        "pip",
        "install",
        "-t",
        PACKAGE_INSTALL_LOCATION,
        ".",
    ],
    "node": [
        "npx",
        "esbuild",
        "--bundle",
        "--minify",
        "--keep-names",
        "--sourcemap",
        "--sources-content=false",
        "--target=node20",
        "--platform=node",
        f"--outfile={PACKAGE_INSTALL_LOCATION}/index.js",
        "src/index.ts",
    ],
}

COMMANDS_ZIP_PACKAGE = {
    "python": ["zip", "-x", "'*.pyc'", "-r", f"../{PACKAGE_FILE_NAME}", "."],
    "node": ["zip", "-r", f"../{PACKAGE_FILE_NAME}", "."],
}

COMMAND_COPY_ZIP = ["aws", "s3", "cp", PACKAGE_FILE_NAME]

ERROR_MISSING_SOURCE_DIR = (
    "You must set a source directory using 'with-source --source <dir>'"
)
ERROR_MISSING_AWS_CREDENTIALS = "You must set AWS credentials with 'with-credentials'"
ERROR_INCOMPATIBLE_SDK = "You must choose either the 'python' or 'node' SDK"
