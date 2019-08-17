const promisify = (fn, ref) => {
  return (...args) => {
    return new Promise((resolve, reject) => {
      const handler = (err, data) => {
        if (err) reject(err);
        else resolve(data);
      };
      fn.bind(ref, ...[...args, handler])();
    });
  };
};

module.exports = {
  promisify
};
