const express = require('express');
const { body, param } = require('express-validator');
const authenticate = require('../middleware/auth');
const validate = require('../middleware/validate');
const { students, findStudent, findClassroom, nextId } = require('../services/dataStore');

const router = express.Router();

router.use(authenticate);

router.get('/', (req, res) => {
  res.json({ data: students });
});

router.post(
  '/',
  [
    body('firstName').isString().trim().notEmpty().withMessage('firstName es requerido'),
    body('lastName').isString().trim().notEmpty().withMessage('lastName es requerido'),
    body('email').isEmail().withMessage('email inválido'),
    body('classroomId')
      .isString()
      .trim()
      .notEmpty()
      .withMessage('classroomId es requerido')
      .custom((value) => {
        if (!findClassroom(value)) {
          throw new Error('classroomId no existe');
        }
        return true;
      })
  ],
  validate,
  (req, res) => {
    const student = {
      id: nextId(students),
      firstName: req.body.firstName.trim(),
      lastName: req.body.lastName.trim(),
      email: req.body.email.toLowerCase(),
      classroomId: req.body.classroomId.trim()
    };
    students.push(student);
    res.status(201).json({ data: student });
  }
);

router.put(
  '/:id',
  [
    param('id').isString().notEmpty(),
    body('firstName').optional().isString().trim().notEmpty(),
    body('lastName').optional().isString().trim().notEmpty(),
    body('email').optional().isEmail(),
    body('classroomId')
      .optional()
      .isString()
      .trim()
      .notEmpty()
      .custom((value) => {
        if (!findClassroom(value)) {
          throw new Error('classroomId no existe');
        }
        return true;
      })
  ],
  validate,
  (req, res) => {
    const student = findStudent(req.params.id);
    if (!student) {
      return res.status(404).json({ message: 'Estudiante no encontrado' });
    }

    if (req.body.firstName) student.firstName = req.body.firstName.trim();
    if (req.body.lastName) student.lastName = req.body.lastName.trim();
    if (req.body.email) student.email = req.body.email.toLowerCase();
    if (req.body.classroomId) student.classroomId = req.body.classroomId.trim();

    res.json({ data: student });
  }
);

router.delete(
  '/:id',
  [param('id').isString().notEmpty()],
  validate,
  (req, res) => {
    const index = students.findIndex((student) => student.id === req.params.id);
    if (index === -1) {
      return res.status(404).json({ message: 'Estudiante no encontrado' });
    }
    const [removed] = students.splice(index, 1);
    res.json({ data: removed });
  }
);

module.exports = router;
