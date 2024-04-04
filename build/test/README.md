Simple Dockerfile to test Dagger building Dockerfiles

To build:

`dagger call with-build-arg --key VERSION --value 3.17 build --dir ./test/`

To test:

`dagger call with-build-arg --key VERSION --value 3.19 build --dir ./test/ with-exec --args "cat,/etc/os-release" stdout`
