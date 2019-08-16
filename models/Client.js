const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const schema = new Schema({
  name: String,
  apiKeyHash: String /* It's actually a uuid but whatever */,
  date: Date
});

return new mongoose.model("client", schema);
