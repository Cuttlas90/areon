'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    Id: DataTypes.INTEGER,
    Email: DataTypes.STRING,
    Nonce: DataTypes.STRING,
    //NonceDateTime: 'DATETIME',
    NonceTimestamp: 'BIGINT',
    Status: DataTypes.INTEGER,
    LastCredit: DataTypes.INTEGER,
//    LastQueryDateTime: 'DATETIME',
    LastQueryTimestamp: 'BIGINT',
    QueryCount: DataTypes.INTEGER,
  }, {timestamps:false,tableName:'user'});
  User.associate = function(models) {
    // associations can be defined here
  };
  return User;
};
