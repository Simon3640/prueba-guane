from .base import BaseErrors


class UserErrors(BaseErrors):
    pass

income_400 = UserErrors(400, "Bad request")

income_401 = UserErrors(401, "No autorizado")

income_403 = UserErrors(403, "Metodo no autorizado")

income_404 = UserErrors(404, "No encontrado")

income_422 = UserErrors(422, "Esta entidad no se puede procesar")