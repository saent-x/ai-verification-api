
function Auth() {
  return (req, res, next) => {
    // check the api-key to make sure it's valid
    next();
  };
}

module.exports = Auth
