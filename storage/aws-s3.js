const AWS = require("aws-sdk");

const s3 = new AWS.S3({
  accessKeyId: "AKIA6LDH3NV7QYAJYPUM",
  secretAccessKey: "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"
});

const listDirectories = () => {
  return new Promise((resolve, reject) => {
    const s3params = {
      Bucket: "document-verification-test-bucket",
      MaxKeys: 20,
      Delimiter: "/"
    };
    s3.listObjectsV2(s3params, (err, data) => {
      if (err) {
        reject(err);
      }
      resolve(data["CommonPrefixes"].map(x => x.Prefix));
    });
  });
};

const downloadFile = (filePath, bucketName, key) => {
  const params = {
    Bucket: bucketName,
    Key: key
  };
  s3.getObject(params, (err, data) => {
    if (err) console.error(err);
    fs.writeFileSync(filePath, data.Body.toString());
    console.log(`${filePath} has been created!`);
  });
};

listDirectories(s3)
  .then(keys => console.log(keys))
  .catch(err => console.log("Unable to fetch keys"));
