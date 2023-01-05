from aiohttp import ClientSession

async def get_session():
    try:
        session = ClientSession()
        yield session
    finally:
        await session.close()