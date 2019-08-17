const express = require("express");
const uuid = require("uuid/v4");
const Joi = require("joi");
const { fetchImagesFromAzure } = require("../azure-helper")

const route = express.Router();

const sharedSchema = {
    prefix: Joi.string().required(),
    mode: Joi.string().valid(["identity", "verification"]).required(),
    storageType: Joi.string().valid(["azure", "s3", "headless"]).default("headless")
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

    console.log("Fetching images from azure...")
    const images = await fetchImagesFromAzure(value.storageName, value.accessKey, value.containerName, value.prefix)
    res.send({ result: images.map(i => i.name) })
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