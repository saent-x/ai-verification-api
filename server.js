require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const register = require("./routes/register");

const PORT = process.env.PORT || 9877;

const app = express();

const mongoose = require("mongoose");
mongoose
  .connect("mongodb://localhost:27017/test", { useNewUrlParser: true })
  .then(() => console.log("Database connection successful!"))
  .catch(err => console.error("Unable to connnect to the database"));

/* Use helmet to secure the api */
app.use(helmet());

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
