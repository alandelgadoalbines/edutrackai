const { verifyToken } = require('../utils/jwt');
const { getUserByEmail } = require('../data/users');
const config = require('../config');
const { sendJson } = require('../utils/http');

function extractTokenFromHeader(req) {
  const authHeader = req.headers.authorization || '';
  const [scheme, token] = authHeader.split(' ');
  if (scheme === 'Bearer' && token) {
    return token.trim();
  }
  return null;
}

function requireAuth(req, res, allowedRoles = []) {
  const token = extractTokenFromHeader(req);
  if (!token) {
    sendJson(res, 401, { message: 'Token no encontrado. Incluya el header Authorization: Bearer <token>.' });
    return null;
  }
  const payload = verifyToken(token, config.jwtSecret);
  if (!payload) {
    sendJson(res, 401, { message: 'Token inválido o expirado.' });
    return null;
  }
  const user = getUserByEmail(payload.email);
  if (!user) {
    sendJson(res, 401, { message: 'Usuario no encontrado.' });
    return null;
  }
  if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    sendJson(res, 403, { message: 'No tiene permisos para acceder a este recurso.' });
    return null;
  }
  return { ...user, tokenPayload: payload };
}

module.exports = {
  requireAuth,
};
