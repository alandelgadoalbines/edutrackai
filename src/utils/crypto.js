const crypto = require('crypto');

const SALT_LENGTH = 16;
const KEY_LENGTH = 64;
const ITERATIONS = 16384;

function hashPassword(password) {
  const salt = crypto.randomBytes(SALT_LENGTH).toString('hex');
  const derivedKey = crypto.scryptSync(password, salt, KEY_LENGTH, { N: ITERATIONS });
  return `${salt}:${derivedKey.toString('hex')}`;
}

function verifyPassword(password, storedHash) {
  const [salt, hash] = storedHash.split(':');
  if (!salt || !hash) {
    return false;
  }
  const derivedKey = crypto.scryptSync(password, salt, KEY_LENGTH, { N: ITERATIONS }).toString('hex');
  return crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(derivedKey, 'hex'));
}

module.exports = {
  hashPassword,
  verifyPassword,
};
