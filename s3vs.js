const AWS = require("aws-sdk");

const SPACE_URL = "fra1.digitaloceanspaces.com";
const SPACE_BUCKET_NAME = "topify-research";
const SPACE_ACCESS_KEY = "CLHSHSLW3ZQZ7SXSFC7Q";
const SPACE_SECRET_ACCESS_KEY = "m9EnA3VFVHQzgxF2rWhSUCwxkLWqNSlMMAfJj7sjGIg";

const spacesEndpoint = new AWS.Endpoint(SPACE_URL);

const s3 = new AWS.S3({
    endpoint: spacesEndpoint,
    accessKeyId: SPACE_ACCESS_KEY,
    secretAccessKey: SPACE_SECRET_ACCESS_KEY,
    signatureVersion: "v4"
});

s3.putBucketCors(
    {
        Bucket: SPACE_BUCKET_NAME,
        CORSConfiguration: {
            CORSRules: [
                {
                    AllowedHeaders: ["*"],
                    AllowedMethods: ["GET", "PUT"],
                    AllowedOrigins: ["*"] //TODO: for prod remove *
                }
            ]
        }
    },
    err => {
        if (err) throw err;
    }
);

const getParams = {
    Bucket: SPACE_BUCKET_NAME,
    Key: "keras/interior_design/interior_design_model.json"
};

(async () => {
    const response = await s3.getObject(getParams).promise();

    console.log(response);
})();
