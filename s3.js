const rp = require("request-promise");

const SPACE_URL = "fra1.digitaloceanspaces.com";
const SPACE_BUCKET_NAME = "topify-research";
const SPACE_ACCESS_KEY = "CLHSHSLW3ZQZ7SXSFC7Q";
const SPACE_SECRET_ACCESS_KEY = "m9EnA3VFVHQzgxF2rWhSUCwxkLWqNSlMMAfJj7sjGIg";

const http = require("http");
const fs = require("fs");
const aws4 = require("aws4")

const opts = {
    host: SPACE_URL,
    service: "s3",
    method: 'GET',
};

aws4.sign(opts, {accessKeyId: SPACE_ACCESS_KEY, secretAccessKey: SPACE_SECRET_ACCESS_KEY});
aws4.sign({service: 's3', path: `/${SPACE_BUCKET_NAME}`, signQuery: true});

aws4.sign(opts);

(async () => {
    try {
        const response = await rp(Object.assign({}, opts,{uri: `https://${opts.host}`}));

        // console.log(response.body)
    } catch (e) {
        console.log(e)
    }

})();

