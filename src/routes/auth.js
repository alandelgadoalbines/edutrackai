const express = require('express');
const jwt = require('jsonwebtoken');
const { body } = require('express-validator');
const validate = require('../middleware/validate');

const router = express.Router();

router.post(
  '/token',
  [body('username').isString().trim().notEmpty(), body('role').optional().isString().trim()],
  validate,
  (req, res) => {
    const payload = { username: req.body.username, role: req.body.role || 'teacher' };
    const token = jwt.sign(payload, process.env.JWT_SECRET || 'dev-secret', { expiresIn: '1h' });
    res.json({ token });
  }
);

module.exports = router;
