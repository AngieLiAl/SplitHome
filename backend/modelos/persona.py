# ──────────────────────────────────────────────────────────────
# MODELO — Persona
# Representa a un miembro del hogar que participa en los gastos.
# ──────────────────────────────────────────────────────────────
class Persona:
    def __init__(self, nombre, email):
        self.id     = None  # el DAO asigna el ID al insertar
        self._nombre = nombre
        self._email  = email

    # ── Encapsulamiento: getters y setters con validación ──────
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = v.strip()

    @property
    def email(self): return self._email
    @email.setter
    def email(self, v):
        if v and "@" not in v:
            raise ValueError("Email inválido")
        self._email = v

    def __str__(self):
        return f"[{self.id}] {self._nombre} | {self._email}"