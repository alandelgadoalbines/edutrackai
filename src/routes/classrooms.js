const express = require('express');
const { body } = require('express-validator');
const authenticate = require('../middleware/auth');
const validate = require('../middleware/validate');
const { classrooms, nextId } = require('../services/dataStore');

const router = express.Router();

router.use(authenticate);

router.get('/', (req, res) => {
  res.json({ data: classrooms });
});

router.post(
  '/',
  [
    body('grade').isInt({ min: 1 }).withMessage('grade debe ser un número entero >= 1'),
    body('section').isString().trim().notEmpty().withMessage('section es requerida')
  ],
  validate,
  (req, res) => {
    const classroom = { id: nextId(classrooms), grade: Number(req.body.grade), section: req.body.section.trim() };
    classrooms.push(classroom);
    res.status(201).json({ data: classroom });
  }
);

module.exports = router;
