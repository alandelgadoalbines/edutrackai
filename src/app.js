const express = require('express');
const morgan = require('morgan');
const studentsRouter = require('./routes/students');
const classroomsRouter = require('./routes/classrooms');
const authRouter = require('./routes/auth');

const app = express();

app.use(express.json());
app.use(morgan('dev'));

app.use('/api/auth', authRouter);
app.use('/api/students', studentsRouter);
app.use('/api/classrooms', classroomsRouter);

app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ message: err.message || 'Internal Server Error' });
});

module.exports = app;
