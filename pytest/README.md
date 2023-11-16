# Dagger Module Test: pytest-ci-module

Can be tested with [pytest-app](https://github.com/mjb141/pytest-app)
To call this module (in a directory with a python app + pytests):

* `dagger call -m "github.com/mjb141/daggerverse/pytest@main" --help`

## Demonstration commands

#### Simple functions (first iteration)

* Pip: `dagger call -m "github.com/mjb141/daggerverse/pytest@simple" pytest-with-pip --src-dir . --tests-dir tests --requirements-files requirements.txt`

* Poetry: `dagger call -m "github.com/mjb141/daggerverse/pytest@simple" pytest-with-poetry --src-dir . --tests-dir tests`

#### Chained functions (second iteration)

* Pip: `dagger call -m "github.com/mjb141/daggerverse/pytest@chained-methods" with-pip --requirements-files requirements.txt test --src-dir . --tests-dir tests`

* Poetry: `dagger call -m "github.com/mjb141/daggerverse/pytest@chained-methods" with-poetry test --src-dir . --tests-dir tests`
