const { hashPassword } = require('../utils/crypto');
const config = require('../config');

const roles = ['admin', 'docente', 'administrativo'];

const users = [
  {
    id: '1',
    email: 'admin@example.com',
    role: 'admin',
    passwordHash: hashPassword(config.adminPassword),
    displayName: 'Administrador Inicial',
  },
];

function getUserByEmail(email) {
  return users.find((user) => user.email.toLowerCase() === email.toLowerCase());
}

module.exports = {
  roles,
  users,
  getUserByEmail,
};
