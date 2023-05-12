from __future__ import annotations
from django.conf import settings



class FlyDBReplicaRouter:
    def db_for_read(self, model, **hints) -> str:  # type: ignore [no-untyped-def]
        return "replica" if "replica" in settings.DATABASES else "default"

    def db_for_write(self, model, **hints) -> str:  # type: ignore [no-untyped-def]
        return "default"

    def allow_relation(self, obj1, obj2, **hints) -> bool: # type: ignore [no-untyped-def] # pragma: no cover
        return True

    def allow_migrate(self, db, app_label, **hints) -> bool:  # type: ignore [no-untyped-def] # pragma: no cover
        return True
