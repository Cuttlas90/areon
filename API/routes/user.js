const express = require('express');
const router = express.Router();
const controller = require('../controllers/userController');
const auth = require('../middleware/auth');

router.get('/', function (req, res, next) {
    res.json('user');
});

router.post('/getNonce', controller.getNonce);
router.post('/login', controller.login);
router.post('/runQuery', controller.runQuery);
router.get('/getSchema', controller.getSchema);
router.get('/getUserInfo', auth.auth, controller.getUserInfo);

module.exports = router;