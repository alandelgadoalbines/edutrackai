const DEFAULT_SECRET = 'change-this-secret';

const config = {
  port: process.env.PORT || 3000,
  jwtSecret: process.env.JWT_SECRET || DEFAULT_SECRET,
  tokenExpiresInSeconds: parseInt(process.env.JWT_EXPIRES_IN || '3600', 10),
  adminPassword: process.env.ADMIN_PASSWORD || 'Admin123!',
};

module.exports = config;
