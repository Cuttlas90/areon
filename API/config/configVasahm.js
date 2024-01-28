const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  development: {
    username: process.env.VASAHM_DB_USER,
    password: process.env.VASAHM_DB_PASSWORD,
    database: process.env.VASAHM_DB_NAME,
    host: process.env.VASAHM_DB_HOST,
    dialect: process.env.VASAHM_DB_DIALECT,
    dialectOptions: {
      port: process.env.VASAHM_DB_PORT
    }
  },
  test: {
    username: process.env.VASAHM_DB_USER,
    password: process.env.VASAHM_DB_PASSWORD,
    database: process.env.VASAHM_DB_NAME,
    host: process.env.VASAHM_DB_HOST,
    dialect: process.env.VASAHM_DB_DIALECT,
    dialectOptions: {
      port: process.env.VASAHM_DB_PORT
    }
  },
  production: {
    username: process.env.VASAHM_DB_USER,
    password: process.env.VASAHM_DB_PASSWORD,
    database: process.env.VASAHM_DB_NAME,
    host: process.env.VASAHM_DB_HOST,
    dialect: process.env.VASAHM_DB_DIALECT,
    dialectOptions: {
      port: process.env.VASAHM_DB_PORT
    }
  }
}