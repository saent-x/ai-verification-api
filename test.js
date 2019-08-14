const { PythonShell } = require("python-shell");

const payload = {
  prefix: "123456",
  storageType: "azure"
};

let options = {
  mode: "text",
  pythonPath: PythonShell.defaultPythonPath,
  pythonOptions: ["-u"], // get print results in real-time
  scriptPath: "py/",
  mode: "json"
};

const pyShell = PythonShell.run("identify.py", options);

pyShell.send(payload);
