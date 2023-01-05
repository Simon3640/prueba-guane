from .app import AppSettings


# Aquí cuando estemos en producción
class ProductionAppSettings(AppSettings):
    debug: bool = False
    title: str = "FastAPI prueba-guane database production"

    class Config:
        env_file = "prod.env"
