const {PythonShell} = require("python-shell");

const payload = {
    prefix: "123456",
    storageType: "azure"
}

let options = {
  mode: 'text',
  pythonPath: PythonShell.defaultPythonPath,
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: 'native/',
  args: [JSON.stringify(payload)]
};

PythonShell.run('identify.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});