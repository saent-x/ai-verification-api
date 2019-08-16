require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const register = require("./routes/register");
const mongoose = require("mongoose");
const auth = require("./middleware/auth");
const bodyParser = require("body-parser");

const PORT = process.env.PORT || 9877;

const CONN_STRING = process.env.CONN_STRING

mongoose
  .connect(CONN_STRING, { useNewUrlParser: true })
  .then(() => console.log("Database connection successful!"))
  .catch(err => console.error("Unable to connnect to the database"));

/* Configure the middleware pipeline*/
const app = express();

app.use(bodyParser.json());
app.use(helmet());
app.use(auth());

app.use("/register", register);

app.get("/", (req, res) =>
  res.send(
    cowsay.think({
      text: "I'm a moooodule",
      e: "oO",
      T: "U "
    })
  )
);

app.listen(PORT);

console.log(`Server running on port ${PORT}`);
