const AWS = require("aws-sdk");
const fs = require("fs");

const SPACE_URL = process.env.SPACE_URL;
const SPACE_BUCKET_NAME = process.env.SPACE_BUCKET_NAME;
const SPACE_ACCESS_KEY = process.env.SPACE_ACCESS_KEY;
const SPACE_SECRET_ACCESS_KEY = process.env.SPACE_SECRET_ACCESS_KEY;

const spacesEndpoint = new AWS.Endpoint(SPACE_URL);

const s3 = new AWS.S3({
    endpoint: spacesEndpoint,
    accessKeyId: SPACE_ACCESS_KEY,
    secretAccessKey: SPACE_SECRET_ACCESS_KEY,
    signatureVersion: 'v4'
});

// Add a file to a Space
const params = {
    Bucket: SPACE_BUCKET_NAME,
    Key: "keras/interior_style/model.h5",
};

s3.getObject(params, function (err, data) {
    if (err) {
        console.log(err, err.stack);
        return;
    }

    fs.writeFile("./data/model.h5", data, () => {
        if (err) {
            return console.log(err);
        }

        console.log("The file was saved!");
    });
});