const { PythonShell } = require("python-shell");

const arguments = {
  prefix: "012345",
  storage: "azure",
  mode: "identification",
  connectionString: "DefaultEndpointsProtocol=https;AccountName=mintfintechrgdiag431;AccountKey=j642+deFffJ5aQED0VjLwC54l/hWb7rclvWEidoHjwGg8EsORRNB8fOa8R12iO74FeS1gLs3SwDaMv2lRRPUuw==;EndpointSuffix=core.windows.net",
  container: "1029380128"
};

const options = {
  mode: "text",
  pythonPath: PythonShell.defaultPythonPath,
  pythonOptions: ["-u"],
  scriptPath: "py/",
  args: [JSON.stringify(arguments)]
};

const pyshell = new PythonShell("bootstrap.py", options);

pyshell.on("message", message => {
  console.log(message);
});
