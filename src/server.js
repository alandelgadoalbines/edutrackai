const http = require('http');
const { parse } = require('url');
const config = require('./config');
const { getUserByEmail, roles } = require('./data/users');
const { verifyPassword } = require('./utils/crypto');
const { generateToken } = require('./utils/jwt');
const { requireAuth } = require('./middleware/auth');
const { sendJson, parseJsonBody } = require('./utils/http');

async function handleLogin(req, res) {
  try {
    const body = await parseJsonBody(req);
    const { email, password } = body;
    if (!email || !password) {
      sendJson(res, 400, { message: 'Debe enviar email y password.' });
      return;
    }
    const user = getUserByEmail(email);
    if (!user || !verifyPassword(password, user.passwordHash)) {
      sendJson(res, 401, { message: 'Credenciales inválidas.' });
      return;
    }
    const token = generateToken(
      { email: user.email, role: user.role, sub: user.id },
      config.jwtSecret,
      config.tokenExpiresInSeconds,
    );
    sendJson(res, 200, {
      token,
      expiresIn: config.tokenExpiresInSeconds,
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        displayName: user.displayName,
      },
    });
  } catch (error) {
    sendJson(res, 400, { message: error.message || 'No se pudo procesar la petición.' });
  }
}

function handleMe(req, res) {
  const user = requireAuth(req, res);
  if (!user) return;
  sendJson(res, 200, {
    id: user.id,
    email: user.email,
    role: user.role,
    displayName: user.displayName,
  });
}

function handleAdminExample(req, res) {
  const user = requireAuth(req, res, ['admin']);
  if (!user) return;
  sendJson(res, 200, { message: `Hola ${user.displayName}, acceso admin concedido.` });
}

function handleRoles(req, res) {
  sendJson(res, 200, { roles });
}

const server = http.createServer((req, res) => {
  const parsedUrl = parse(req.url, true);
  const { pathname } = parsedUrl;

  if (req.method === 'POST' && pathname === '/api/auth/login') {
    handleLogin(req, res);
    return;
  }

  if (req.method === 'GET' && pathname === '/api/auth/roles') {
    handleRoles(req, res);
    return;
  }

  if (req.method === 'GET' && pathname === '/api/auth/me') {
    handleMe(req, res);
    return;
  }

  if (req.method === 'GET' && pathname === '/api/admin/example') {
    handleAdminExample(req, res);
    return;
  }

  sendJson(res, 404, { message: 'Ruta no encontrada' });
});

server.listen(config.port, () => {
  if (config.jwtSecret === 'change-this-secret') {
    // eslint-disable-next-line no-console
    console.warn('ADVERTENCIA: configure JWT_SECRET para un entorno seguro.');
  }
  // eslint-disable-next-line no-console
  console.log(`Servidor escuchando en puerto ${config.port}`);
});
