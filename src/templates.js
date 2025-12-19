const DEFAULT_TEMPLATE =
  "Asistencia diaria {{date}}: Hola {{name}}, confirma tu presencia respondiendo a este mensaje.";

function buildMessage({ studentName, date, template = DEFAULT_TEMPLATE }) {
  const name = (studentName || "estudiante").trim();
  const formattedDate = (date || new Date().toLocaleDateString("es-ES")).trim();

  return template
    .replace(/{{\s*name\s*}}/gi, name)
    .replace(/{{\s*date\s*}}/gi, formattedDate);
}

module.exports = {
  DEFAULT_TEMPLATE,
  buildMessage,
};
