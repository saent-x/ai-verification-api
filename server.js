require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const mongoose = require("mongoose");
const auth = require("./middleware/auth");
const bodyParser = require("body-parser");
const verification = require("./routes/verification");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 9877;

const CONN_STRING = process.env.CONN_STRING

mongoose
  .connect(CONN_STRING, { useNewUrlParser: true })
  .then(() => console.log("Database connection successful!"))
  .catch(() => console.error("Unable to connnect to the database"));

/* Configure the middleware pipeline */
const app = express();

app.use(bodyParser.json());
app.use(helmet());
app.use(auth());

app.use("/verification", verification);

app.get("/", (_, res) =>
  res.type("html").send(fs.readFileSync(path.join(__dirname, "/pages/welcome.html")))
);

app.listen(PORT);

console.log(`Server running on port ${PORT}`);
