const http = require('http');
const rp = require("request-promise").defaults({encoding: null});
//
let chunks = {};
// let buffer = [];
//
const url = "http://www.smalldesignideas.com/wp-content/uploads/2018/10/industr_003.jpg";

[...new Array(1000).keys()]
    .map(async (i) => {
        const body = await rp(url)

        console.log(body.length)
        // const body = rp(url)
        //     .on("data", (chunk) => {
        //         if (!chunks[i]) {
        //              chunks[i] = [];
        //         }
        //         chunks[i] += chunk
        //     })
        //     .on("end", () => {
        //         console.log(chunks[i].length)
        //         // chunks = [];
        //     })


        // http.get(url, (resp) => {
        //     resp.on('data', (chunk) => {
        //         chunks += chunk
        //     });
        //     resp.on('end', (x) => {
        //         console.log(chunks.length);
        //         chunks = [];
        //         //return res.json({result: body, status: 'success'});
        //     });
        // }).on('error', (e) => {
        //     console.log(`Got error: ${e.message}`);
        // });
    });
