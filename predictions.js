const rp = require("request-promise").defaults({encoding: null});

const fs = require("fs");
const tf = require("@tensorflow/tfjs-node");
const tfn = require("@tensorflow/tfjs-node");

const handler = tfn.io.fileSystem("./data/tf2/interior-style/model.json");

global.fetch = require('node-fetch');

const labels = [
    "bohemian",
    "classic",
    "coastal",
    "farm-house",
    "glam",
    "industrial",
    "mid-century-modern",
    "minimal",
    "preppy",
    "rustic",
    "scandinavian",
    "transitional"
];

const url = "https://scontent.fpoz2-1.fna.fbcdn.net/v/t1.0-9/78450257_2561393933914551_5972082700020875264_o.jpg?_nc_cat=100&_nc_ohc=7LQR1ha7bG4AQn7-BeyuiYhwFKvzd3_lL1P_Nm7PLUzN_9VqWJJOweU3g&_nc_ht=scontent.fpoz2-1.fna&oh=7eb51898afa07d075625d0f71b2ea30e&oe=5E7577F8";
// let buffer = [];

const readImage = async path => {
    // const imageBuffer = fs.readFileSync(path);
    const body = await rp(url);

    return tf.node.decodeImage(body)
        .resizeNearestNeighbor([150, 150])
        .toFloat()
        .div(255)
        .expandDims();

    // return new Promise((resolve, reject) => {
    //     const imageBuffer = rp(p, (err, res, body) => {
    //         return path
    //         console.log(path);
    //
    //         if (err) {
    //             return reject(err);
    //         }
    //
    //         resolve(x);
    //     });
    // });
};

const predict = async (model) => {
    const tensorImg = await readImage("./data/images/rustic0.jpg");

    return model
        .predict(tensorImg)
        .data()
};

(async () => {
    const model = await tf.loadLayersModel(handler);

    await Promise.all([...new Array(1000).keys()]
        .map(async () => {
            const predictions = await predict(model);

            const labeledPredictions = (new Array(...predictions))
                .map((prediction, i) => ({
                    prediction,
                    label: labels[i]
                }))
                .sort((a, b) => b.prediction - a.prediction);

            // console.log(!!labeledPredictions);
            // console.log(labeledPredictions);

            console.log(true)
        }));

    console.log("FINISH")
    // console.log(labeledPredictions);
})();
