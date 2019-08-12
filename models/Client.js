const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const schema = new Schema({
  storageType: String,
  apiKeyHsh: String /* It's actually a uuid but whatever */,
  body: String,
  date: Date
});

return new mongoose.model("client", schema);
