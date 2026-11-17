# Overlay para TikTok LIVE

Overlay vertical (1080×1920) con alertas, metas y top de regalos. Se conecta a los eventos de TikFinity en `ws://localhost:21213`, así que TikFinity debe estar abierto durante el directo.

Parámetros de la URL:
- `seg`: meta de seguidores (por defecto 30; sube +30 al cumplirse)
- `likes`: meta de likes (por defecto 10000; se duplica al cumplirse)
- `sonido=0`: desactiva los sonidos del overlay
- `demo=1&fondo=1`: modo demostración con fondo, para probar el diseño

## Uso en TikTok LIVE Studio

Los navegadores bloquean que una página de internet se conecte a programas del propio PC ("Local Network Access"), así que el overlay se sirve en local:

```
pythonw servidor.py
```

y en LIVE Studio se añade como Enlace: `http://localhost:21300/` (resolución 1080×1920).
La versión de GitHub Pages sirve para ver el diseño en modo demo: `?demo=1&fondo=1`.
