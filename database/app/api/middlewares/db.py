from tortoise import connections


async def get_db():
    try:
        db = connections.get("default")
        yield db
    finally:
        await db.close()
