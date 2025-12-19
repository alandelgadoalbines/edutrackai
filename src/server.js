const http = require("http");
const { URL } = require("url");
const { buildMessage, DEFAULT_TEMPLATE } = require("./templates");

const PORT = process.env.PORT || 3000;
const CONFIG = {
  apiUrl: process.env.WHATSAPP_API_URL,
  token: process.env.WHATSAPP_TOKEN,
  from: process.env.WHATSAPP_FROM,
  template: process.env.WHATSAPP_TEMPLATE || DEFAULT_TEMPLATE,
};

function sendJson(res, status, body) {
  const data = JSON.stringify(body);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(data),
  });
  res.end(data);
}

function isConfigured() {
  return Boolean(CONFIG.apiUrl && CONFIG.token);
}

async function sendWhatsAppMessage({ to, studentName, date }) {
  const message = buildMessage({
    studentName,
    date,
    template: CONFIG.template,
  });

  const payload = {
    to,
    type: "text",
    text: { body: message },
  };

  if (CONFIG.from) {
    payload.from = CONFIG.from;
  }

  const response = await fetch(CONFIG.apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${CONFIG.token}`,
    },
    body: JSON.stringify(payload),
  });

  const responseBody = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error("WhatsApp API responded with an error");
    error.details = responseBody;
    throw error;
  }

  return { providerResponse: responseBody, preview: message };
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1e6) {
        req.connection.destroy();
        reject(new Error("Request body too large"));
      }
    });
    req.on("end", () => {
      try {
        const parsed = JSON.parse(body || "{}");
        resolve(parsed);
      } catch (error) {
        reject(error);
      }
    });
    req.on("error", reject);
  });
}

const server = http.createServer(async (req, res) => {
  const { pathname } = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === "POST" && pathname === "/api/whatsapp/send") {
    if (!isConfigured()) {
      return sendJson(res, 500, {
        error:
          "La API de WhatsApp no está configurada. Define WHATSAPP_API_URL y WHATSAPP_TOKEN.",
      });
    }

    try {
      const body = await parseJsonBody(req);
      const { to, studentName, date } = body;

      if (!to) {
        return sendJson(res, 400, {
          error: "Falta el número de destino 'to' en el cuerpo de la petición.",
        });
      }

      const result = await sendWhatsAppMessage({ to, studentName, date });
      return sendJson(res, 200, {
        message: "Mensaje enviado",
        to,
        preview: result.preview,
        providerResponse: result.providerResponse,
      });
    } catch (error) {
      const status = error instanceof SyntaxError ? 400 : 502;
      const errorMessage =
        error instanceof SyntaxError
          ? "Cuerpo JSON inválido"
          : "No se pudo enviar el mensaje";

      return sendJson(res, status, {
        error: errorMessage,
        details: error.details || error.message,
      });
    }
  }

  if (req.method === "GET" && pathname === "/") {
    return sendJson(res, 200, {
      status: "ok",
      info: "Servicio de mensajería de asistencia diaria",
    });
  }

  sendJson(res, 404, { error: "Ruta no encontrada" });
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Servidor escuchando en el puerto ${PORT}`);
  });
}

module.exports = server;
