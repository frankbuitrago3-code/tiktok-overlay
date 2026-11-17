"""Sirve el overlay en http://localhost:21300 (solo para este PC).

LIVE Studio carga el overlay desde aquí. Al servirse desde localhost, el navegador
permite que se conecte a TikFinity (ws://localhost:21213).
Se puede ejecutar con pythonw (sin ventana).
"""
import functools
import http.server
import os
import socketserver

PUERTO = 21300
CARPETA = os.path.dirname(os.path.abspath(__file__))


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # pythonw no tiene consola donde escribir
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        # LIVE Studio comprueba el enlace con una petición desde su propia app.
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


class Servidor(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    manejador = functools.partial(Silencioso, directory=CARPETA)
    try:
        with Servidor(("127.0.0.1", PUERTO), manejador) as servidor:
            servidor.serve_forever()
    except OSError:
        pass  # ya hay otro servidor del overlay funcionando
