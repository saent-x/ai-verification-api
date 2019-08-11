const express = require("express");
const uuid = require("uuid/v4");

const route = express.Router();

route.post("/", (req, res) => {
    res.send({ "api-key": uuid() })
});

module.exports = route