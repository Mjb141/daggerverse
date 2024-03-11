# Sample Typescript Lambda app

* Authenticate with AWS in your terminal

### To prepare for Lambda:

* `npm run clean` (removes `dist/` directory if it exists)
* `npm run build` (creates the `dist/` directory with the build javascript file(s))
* `npm run zip` (zips up the contents of the `dist/` directory)

The resulting `lambda.zip` should be uploaded to Lambda. 

**Note**: The handler for the function must be set to `index.handler`
This is formed of: 
* `index` (the file name that contains the entry function)
* `handler` (the function name for the entry point)

### To use from Dagger:

#### Building:
* `dagger call -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk node with-source --source . build`

#### Interactive shell:
* `dagger shell -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk node with-source --source . build`

#### Export the zip for Lambda:
* `dagger download -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk node with-source --source . export`

#### Publish the zip to S3:
* `dagger call -m "github.com/mjb141/daggerverse/lambda@main" with-credentials --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY --ses-token $AWS_SESSION_TOKEN with-sdk --sdk node with-source --source . publish --bucket_name $BUCKET_NAME --object-key $OBJECT_NAME`
