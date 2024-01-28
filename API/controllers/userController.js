let uuid = require("uuid");
let model = require('../models/index');
let vasahmDb = require('../models/indexVasahm');
const jwt = require('jsonwebtoken');
const { Op } = require("sequelize");
const dotenv = require('dotenv');
var nodemailer = require('nodemailer');
dotenv.config();

module.exports = {
    getNonce: async function (req, res, next) {
        let user = await model.User.findOne({ where: { Email: req.body.Email } });
        var nonce = Math.floor(1000 + Math.random() * 9000).toString();
        console.log(nonce)
        if (user) {
            user.Nonce = nonce;
            let date = new Date();
            user.NonceTimestamp = date.getTime();
            user.NonceDateTime = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
            user.save()
                .then(user => {
                    var transporter = nodemailer.createTransport({
                        host: "smtp.zoho.com",
                        port: 587,
                        // secure: true,
                        auth: {
                            user: "info@vasahm.com",
                            pass: "tXYHj5SwghG8"
                        },
                        tls: {
                            // do not fail on invalid certs
                            rejectUnauthorized: false
                          },
                          from: "info@vasahm.com"
                    });
                    
                    var mailOptions = {
                        from: "Vasahm <info@vasahm.com>",
                        to: req.body.Email,
                        subject: 'Vasahm Verification Code',
                        html: '<!DOCTYPE html>'+
                        '<html><head><title>Vasahm Verification Code</title>'+
                        '</head><body><div>'+
                        '<p style="text-align: center; font-weight: bold;">Your Verification code :</p>'+
                        '<p style="text-align: center; font-size: xx-large; font-weight: bolder;">'+ nonce +'</p>'+
                        '</div></body></html>' 
                    };
                    transporter.sendMail(mailOptions, function(error, info){
                        if (error) {
                            console.log(error);
                            res.json({ hasError: true, data: {}, error: error })
                        } else {
                            console.log('Email sent: ' + info.response);
                            res.json({ hasError: false, data: { }, message: 'user created successfully' })
                        }
                    });
                })
                .catch(error => {
                    console.log(error)
                    res.json({ hasError: true, data: {}, error: error })
                });
        }
        else {
            let data = req.body;
            data.Nonce = nonce;
            let date = new Date();
            data.NonceTimestamp = date.getTime();
            data.NonceDateTime = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
            data.LastCredit = process.env.INITIAL_CREDIT;
            model.User.create(data)
                .then(user => {
                    var transporter = nodemailer.createTransport({
                        host: "smtp.zoho.com",
                        port: 587,
                        // secure: true,
                        auth: {
                            user: "info@vasahm.com",
                            pass: "tXYHj5SwghG8"
                        },
                        tls: {
                            // do not fail on invalid certs
                            rejectUnauthorized: false
                          },
                          from: "info@vasahm.com"
                    });
                    
                    var mailOptions = {
                        from: "Vasahm <info@vasahm.com>",
                        to: req.body.Email,
                        subject: 'Vasahm Verification Code',
                        html: '<!DOCTYPE html>'+
                        '<html><head><title>Vasahm Verification Code</title>'+
                        '</head><body><div>'+
                        '<p style="text-align: center; font-weight: bold;">Your Verification code :</p>'+
                        '<p style="text-align: center; font-size: xx-large; font-weight: bolder;">'+ nonce +'</p>'+
                        '</div></body></html>' 
                    };
                    transporter.sendMail(mailOptions, function(error, info){
                        if (error) {
                            console.log(error);
                            res.json({ hasError: true, data: {}, error: error })
                        } else {
                            console.log('Email sent: ' + info.response);
                            res.json({ hasError: false, data: { }, message: 'user created successfully' })
                        }
                    });
                })
                .catch(error => {
                    res.json({ hasError: true, data: {}, error: error })
                });
        }
    },
    login: async function (req, res, next) {
        let user = await model.User.findOne({ where: { Email: req.body.Email } });
        
        if (!user) 
            return res.json({ hasError: true, data: {}, error: {code : 101, message: 'User not found' } });

        if( new Date().getTime() - user.NonceTimestamp > process.env.NONCE_TIMEOUT )
            return res.json({ hasError: true, data: [], error: { code : 102, message: 'time is over.' } })
        //let date = new Date(user.NonceDateTime)
        //console.log(user.NonceDateTime)
        //console.log(date)
        //date = new Date();
        //let str = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
        //console.log(str)
        //date = new Date(str)
        //console.log(date)

        if(user.Nonce == req.body.Nonce)
        {
            let token = jwt.sign({
                data: { Email: user.Email, id: user.Id }
            }, process.env.SECRET, { expiresIn: '1d' });
            user.save()
                .then(user => {
                    res.json({ hasError: false, data: { Token: token, Email: user.Email, UserId: user.Id } });
                })
                .catch(error => {
                    res.json({ hasError: true, data: {}, error: error })
                });
        } 
        else 
        {
            res.json({ hasError: true, data: [], error: { code : 103, message: 'Invalid Nonce' } })
        }
    },
    getUserInfo: async function (req, res, next) {
        let user = await model.User.findOne({ where: { Id: req.UserId } });
        
        if (!user) 
            return res.json({ hasError: true, data: {}, error: {code : 101, message: 'User not found' } });
        res.json({ hasError: false, data: { Email: user.Email, UserId: user.Id, LastCredit : user.LastCredit } });
    },
    runQuery: async function (req, res, next) {
        // let user = await model.User.findOne({ where: { Id: req.UserId } });
        // if (!user) return res.json({ hasError: true, data: {}, error: { message: 'User not found' } });
        // if( new Date().getTime() - user.LastQueryTimestamp < process.env.QUERY_TIME_LIMITATION )
        //     return res.json({ hasError: true, data: [], error: { message: 'query time limitation.' } })
        // if( user.LastCredit < process.env.QUERY_PRICE )
        //     return res.json({ hasError: true, data: [], error: { message: 'credit limitation.' } })
        var queryString = req.body.queryString;
        console.log(queryString)
        vasahmDb.sequelize.query(queryString)
            .then(result => {
                res.json({ hasError: false, data: {result : result[0]}, message: 'run query successfully' })
                // user.LastQueryTimestamp = new Date().getTime();
                // user.LastCredit = user.LastCredit - process.env.QUERY_PRICE;
                // user.save()
                //     .then(user => {
                //         res.json({ hasError: false, data: {result : result[0]}, message: 'run query successfully' })
                //     })
                //     .catch(error => {
                //         res.json({ hasError: true, data: {}, error: { message: 'system error, please try again.' } })
                //     });
            })
            .catch(error => {
                console.log(error)
                res.json({ hasError: true, data: {}, error: error })
            });
    },
    getSchema: async function (req, res, next) {
        // let user = await model.User.findOne({ where: { Id: req.UserId } });
        // if (!user) return res.json({ hasError: true, data: {}, error: { message: 'User not found' } });
        const result = require(__dirname + '/../config/tables.js');
        //var tableName = req.body.tableName;
        //var queryString = "SELECT COLUMN_NAME as columnName, DATA_TYPE as dataType FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '"+ tableName + "'";
        //var result = await model.sequelize.query(queryString)
        ////var result = await model.sequelize.query("SELECT  input.spentTransactionHash from input")
        //console.log(result)
        res.json({ hasError: false, data: result , message: 'get schema successfully' })
    },
};