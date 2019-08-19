const express = require("express");
const uuid = require("uuid/v4");
const Joi = require("joi");
const { PythonShell } = require("python-shell");
const { fetchImagesFromAzure } = require("../azure-helper")
const path = require("path");


const route = express.Router();

const sharedSchema = {
    prefix: Joi.string().required(),
    mode: Joi.string().valid(["identity", "verification"]).required(),
    storageType: Joi.string().valid(["azure", "s3", "headless"]).default("headless")
}

async function processImages(images) {
    return new Promise((resolve, reject) => {
        const arguments = {
            selfie: images.filter(i => i.indexOf("selfie") != -1)[0],
            ids: images.filter(i => i.indexOf("id") != -1)
        };

        const options = {
            mode: "text",
            pythonPath: "C:\\Users\\Mee\\Anaconda3\\envs\\py36_knime\\python.exe",
            pythonOptions: ["-u"],
            args: [JSON.stringify(arguments)]
        };

        let result = null;

        const pyshell = new PythonShell(path.join(__dirname, "../scripts/process.py"), options);

        pyshell.on("message", message => {
            const msg = JSON.parse(message)
            if (msg.type === "result") {
                result = msg.result;
            }
            else
                console.log(`[python] -> [${msg.type}] ${msg.message}`);
        });

        pyshell.on("close", () => {
            if (result)
                resolve(result)
            else
                reject("Unable to process for some reason")
        });

    });
}

async function handleAzureRequest(req, res) {
    const schema = {
        // extend the shared schema with azure specific fields
        ...sharedSchema,
        storageName: Joi.string().required(),
        accessKey: Joi.string().required(),
        containerName: Joi.string().required()
    }

    const { error, value } = Joi.validate(req.body, schema);
    if (error) {
        // send a 422 error response if validation fails
        res.status(422).json({
            status: 'error',
            message: error.details[0].message,
        })
        return;
    }

    let images = [];
    try {
        console.log("Fetching images from azure...")
        images = await fetchImagesFromAzure(value.storageName, value.accessKey, value.containerName, value.prefix)
    }
    catch (ex) {
        res.status(500).send({ status: "error", message: "Unable to retrieve images from azure" });
    }
    try {
        console.log("Images fetched, now processing...")
        const result = await processImages(images);
        res.send({ status: "success", scores: result })
    }
    catch (error) {
        /* We should never get here */
        res.status(500).send({ status: "error", message: "Unable to process request" });
    }
}

route.post("/", async (req, res) => {
    // peek the storage type 
    const storageType = req.body.storageType;
    if (!storageType) {
        res.status(400).send({
            status: "error",
            message: "StorageType is required"
        });
        return;
    }

    switch (storageType) {
        case "azure":
            return await handleAzureRequest(req, res)
        default:
            schema = { ...sharedSchema }
    }
});

module.exports = route