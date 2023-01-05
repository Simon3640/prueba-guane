from .base import BaseErrors


class UserErrors(BaseErrors):
    pass

expense_400 = UserErrors(400, "Bad request")

expense_401 = UserErrors(401, "No autorizado")

expense_403 = UserErrors(403, "Metodo no autorizado")

expense_404 = UserErrors(404, "No encontrado")

expense_422 = UserErrors(422, "Esta entidad no se puede procesar")