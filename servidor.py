"""Sirve el overlay en http://localtest.me:21300 (solo para este PC).

LIVE Studio carga el overlay desde aquí. Al servirse desde el propio PC, el navegador
permite que se conecte a TikFinity (ws://localhost:21213).
Se puede ejecutar con pythonw (sin ventana).

Pruebas sin estar en directo (el overlay las recoge en /cola):
  http://localtest.me:21300/disparar?tipo=seguidor   (o regalo, epico, compartir, likes, todo)
"""
import functools
import http.server
import json
import os
import socketserver
import threading
import urllib.parse

PUERTO = 21300
CARPETA = os.path.dirname(os.path.abspath(__file__))

_cola = []
_candado = threading.Lock()

GENTE = [
    {"uniqueId": "luna.vibes", "nickname": "Luna ✨", "profilePictureUrl": "https://i.pravatar.cc/150?img=47"},
    {"uniqueId": "el_parcero", "nickname": "El Parcero", "profilePictureUrl": "https://i.pravatar.cc/150?img=12"},
    {"uniqueId": "valen.rd", "nickname": "Valen", "profilePictureUrl": "https://i.pravatar.cc/150?img=32"},
    {"uniqueId": "mariajose", "nickname": "María José", "profilePictureUrl": "https://i.pravatar.cc/150?img=15"},
]
ROSA = "https://p16-webcast.tiktokcdn.com/img/maliva/webcast-va/eba3a9bb85c33e017f3648eaf88d7189~tplv-obj.webp"
UNIVERSO = "https://p16-webcast.tiktokcdn.com/img/maliva/webcast-va/8f471afbcebfda3841a6cc515e381f58~tplv-obj.webp"


def eventos_de_prueba(tipo):
    g = GENTE
    catalogo = {
        "seguidor": [{"event": "follow", "data": g[0]}],
        "regalo": [{"event": "gift", "data": {**g[1], "giftName": "Rosa", "giftId": 5655, "diamondCount": 1,
                                              "repeatCount": 5, "giftType": 1, "repeatEnd": True, "giftPictureUrl": ROSA}}],
        "epico": [{"event": "gift", "data": {**g[3], "giftName": "Universo", "giftId": 7312, "diamondCount": 34999,
                                             "repeatCount": 1, "giftType": 2, "giftPictureUrl": UNIVERSO}}],
        "compartir": [{"event": "share", "data": g[2]}],
        "likes": [{"event": "like", "data": {**g[1], "likeCount": 50, "totalLikeCount": 4200}}],
    }
    if tipo == "todo":
        return [e for k in ("seguidor", "likes", "regalo", "compartir", "epico") for e in catalogo[k]]
    return catalogo.get(tipo, [])


class Manejador(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # pythonw no tiene consola donde escribir
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        # LIVE Studio comprueba el enlace con una petición desde su propia app.
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def _json(self, datos):
        cuerpo = json.dumps(datos).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/cola":
            with _candado:
                pendientes = _cola[:]
                _cola.clear()
            return self._json(pendientes)
        if url.path == "/disparar":
            tipo = urllib.parse.parse_qs(url.query).get("tipo", ["todo"])[0]
            nuevos = eventos_de_prueba(tipo)
            with _candado:
                _cola.extend(nuevos)
            return self._json({"encolados": len(nuevos)})
        return super().do_GET()


class Servidor(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    manejador = functools.partial(Manejador, directory=CARPETA)
    try:
        with Servidor(("127.0.0.1", PUERTO), manejador) as servidor:
            servidor.serve_forever()
    except OSError:
        pass  # ya hay otro servidor del overlay funcionando
