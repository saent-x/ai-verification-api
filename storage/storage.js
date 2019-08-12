const helpers = {
  azure: require("./azure-helper"),
  s3: require("./s3-helper")
};

const STORAGE_SOURCES = {
  AZURE: new Symbol("azure"),
  S3: new Symbol("s3")
};

class Storage {
  fetchFiles(opts) {
    if (!opts) throw new Error("Must specify options parameter");

    if (!opts.id) throw new Error("Id must be specified!");

    if (opts.source === STORAGE_SOURCES.AZURE) {
      /* We're fetching the files from an azure blob */
      if (!opts.connectionString)
        throw new Error("No connection string supplied!");
      return azure.fetchFiles({
        connectionString: opts.connectionString,
        id: opts.id
      });
    } else if (opts.source === STORAGE_SOURCES.S3) {
      if (!opts.accessKeyId) throw new Error("Access key id is required!");
      if (!opts.secretAccessKey)
        throw new Error("Secret Access Key is required!");

      /* We're fetching the files from an s3 bucket */
    }
  }
}
