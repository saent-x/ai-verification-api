var input = ["012345", "azure"];

require("amqplib/callback_api").connect(
  "amqp://kelvin:jerryboyis6@localhost",
  function(err, conn) {
    if (err) {
      console.log(err);
      return;
    }
    conn.createChannel(function(err, ch) {
      var simulations = "simulations";

      ch.assertQueue(simulations, { durable: false });
      var results = "results";
      ch.assertQueue(results, { durable: false });

      ch.sendToQueue(simulations, Buffer.from(JSON.stringify(input)));

      ch.consume(results, function(msg) {
        const result = Buffer.from(msg.content).toString("utf-8");
        console.log(result);
      });
    });
    setTimeout(function() {
      conn.close();
    }, 500);
  }
);
