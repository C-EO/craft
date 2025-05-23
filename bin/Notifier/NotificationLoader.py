import importlib

_NOTIFICATION_BACKENDS = None


def load(modules):
    global _NOTIFICATION_BACKENDS
    if _NOTIFICATION_BACKENDS is None:
        _NOTIFICATION_BACKENDS = dict()
        for backend in modules:
            backend = backend.strip()
            backend = getattr(importlib.import_module(f"Notifier.Backends.{backend}"), backend)()
            _NOTIFICATION_BACKENDS[backend.name] = backend
    return _NOTIFICATION_BACKENDS
