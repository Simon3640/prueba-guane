from .base import BaseErrors


class UserErrors(BaseErrors):
    pass


user_400 = UserErrors(400, "Bad request")

user_401 = UserErrors(401, "No autorizado")

user_403 = UserErrors(403, "Metodo no autorizado")

user_404 = UserErrors(404, "User no encontrado")

user_422 = UserErrors(422, "Esta entidad no se puede procesar")

user_registered = UserErrors(
    409,
    "Este usario no se puede registrar, su nombre de usuario o correo electrónico se encuentra ya registrado",
)

user_diferent_password = UserErrors(401, "El correo o la contraseña están erradas")

user_inactive = UserErrors(
    403,
    "Tu cuenta no se encuentra activa, recuerda revisar tu correo para activarla o pide correo de activación nuevamente",
)
