const {
    Aborter,
    BlockBlobURL,
    ContainerURL,
    ServiceURL,
    SharedKeyCredential,
    StorageURL,
} = require('@azure/storage-blob');
const _ = require("lodash");
const concat = require("concat-stream")
const os = require("os")
const path = require("path")
const fs = require("fs-extra")

const ONE_MINUTE = 60 * 1000;

async function containerExists(containerName, aborter, serviceURL) {
    let response;
    let marker;

    do {
        response = await serviceURL.listContainersSegment(aborter, marker);
        marker = response.marker;
        for (let container of response.containerItems) {
            if (container.name === containerName)
                return true
        }
    } while (marker);

    return false
}

async function getPrefixedBlobs(prefix, aborter, containerURL) {

    let response;
    let marker;
    let results = [];

    do {
        response = await containerURL.listBlobFlatSegment(aborter);
        marker = response.marker;
        for (let blob of response.segment.blobItems) {
            // console.log(` - ${blob.name}`);

            const blobName = blob.name.indexOf('/') != -1 ? blob.name.split("/")[1] : blob.name;

            if (blobName.indexOf("_") != -1 && blobName.split("_")[0] === prefix)
                results.push(blob.name)
        }
    } while (marker);

    return results;
}

function fetchImagesFromAzure(storageName, accessKey, containerName, prefix) {
    return new Promise(async (resolve, reject) => {
        if (!storageName)
            reject(new Error("Storage name cannot be null"))
        if (!accessKey)
            reject(new Error("Access key must be a valid string"))
        if (!containerName)
            reject(new Error("Container nam must be a valid string"))
        if (!prefix)
            reject(new Error("A prefix must be provided"))

        const aborter = Aborter.timeout(30 * ONE_MINUTE);

        const credentials = new SharedKeyCredential(storageName, accessKey);
        const pipeline = StorageURL.newPipeline(credentials);
        const serviceURL = new ServiceURL(`https://${storageName}.blob.core.windows.net`, pipeline);

        if (!await containerExists(containerName, aborter, serviceURL)) {
            reject(new Error("No container with that name found"))
        }

        const containerURL = ContainerURL.fromServiceURL(serviceURL, containerName);
        const prefixedBlobs = await getPrefixedBlobs(prefix, aborter, containerURL)

        // Sanity checks 
        const hasSlefie = _.find(prefixedBlobs, blob => blob.indexOf("selfie") != -1)
        if (!hasSlefie)
            reject(new Error("No selfie found"));

        const hasAtLeastOneId = _.find(prefixedBlobs, blob => blob.indexOf("id") != -1)
        if (!hasAtLeastOneId)
            reject(new Error("At least on ID required"));

        const downloads = []

        for (const blobName of prefixedBlobs) {
            const blockBlobURL = BlockBlobURL.fromContainerURL(containerURL, blobName);
            const downloadResponse = await blockBlobURL.download(aborter, 0);

            downloads.push(new Promise((resolve, reject) => {
                const readStream = downloadResponse.readableStreamBody;
                readStream.on("error", (e) => {
                    reject(Error("Unable to fetch blob data: " + e.message));
                })
                writeStream = concat(async (buffer) => {
                    const file = blobName.replace(/\//g, "-")
                    const outPath = path.join(os.tmpdir(), "azure-cache", file);
                    await fs.outputFile(outPath, buffer, { encoding: "binary" })

                    console.log(`[azure-helper]: fetched ${file}`);
                    resolve(outPath);
                });
                readStream.pipe(writeStream);
            }));
        }

        Promise.all(downloads).then(resolve).catch(reject)
    })
}

module.exports = {
    fetchImagesFromAzure
}