"""Configuration pytest partagée."""

import os

# Les tests n'exportent pas de traces : on évite le bruit des avertissements
# Logfire lorsqu'aucun `logfire.configure()` n'a été appelé.
os.environ.setdefault("LOGFIRE_IGNORE_NO_CONFIG", "1")
