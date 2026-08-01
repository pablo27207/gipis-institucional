"""
Protecciones básicas: rate limiting en memoria por IP.

El límite es por worker de gunicorn (hay 2 en producción), así que el
tope efectivo puede ser hasta el doble del declarado — suficiente contra
bots y fuerza bruta sin agregar dependencias ni estado compartido.
"""
import time
from collections import defaultdict, deque

from flask import request

_hits = defaultdict(deque)
_MAX_KEYS = 10000  # tope de memoria: se purgan colas vencidas si se supera


def client_ip():
    """IP real del cliente detrás de Traefik/nginx (primer X-Forwarded-For)."""
    forwarded = request.headers.get('X-Forwarded-For', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def rate_limited(action, limit, window_seconds):
    """True si la IP superó `limit` intentos de `action` en la ventana dada.

    Cada llamada cuenta como un intento (si no está bloqueada).
    """
    key = f'{action}:{client_ip()}'
    now = time.time()
    q = _hits[key]
    while q and q[0] < now - window_seconds:
        q.popleft()
    if len(q) >= limit:
        return True
    q.append(now)

    if len(_hits) > _MAX_KEYS:
        for k in [k for k, v in _hits.items() if not v]:
            del _hits[k]
    return False
