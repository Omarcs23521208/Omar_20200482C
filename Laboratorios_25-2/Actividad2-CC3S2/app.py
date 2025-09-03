import os
import sys
import logging
import json
from flask import Flask, jsonify, request

# --- Logging: stdout (12-Factor) ---
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)
# Añadir handler si no existe (evita handlers duplicados en reloads)
if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
    root.addHandler(handler)

# Asegurar que Werkzeug (servidor dev) use el mismo comportamiento
logging.getLogger('werkzeug').handlers = root.handlers
logging.getLogger('werkzeug').setLevel(logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # Leer por petición (explica en el REPORT la nota sobre procesos/env)
    message = os.getenv("MESSAGE", "Hola mundo")
    release = os.getenv("RELEASE", "v0")

    payload = {
        "message": message,
        "release": release,
        "method": request.method,
        "path": request.path,
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr)
    }

    # Log legible + log estructurado (JSON por línea)
    logger.info("Acceso a / - message=%s release=%s", message, release)
    logger.info(json.dumps(payload, ensure_ascii=False))

    return jsonify(payload), 200

@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check realizado")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Iniciando aplicación en puerto {port}")
    app.run(host='0.0.0.0', port=port)

