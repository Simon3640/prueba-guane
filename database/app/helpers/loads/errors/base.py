class BaseErrors(Exception):
    def __init__(self, code: int, detail: str):
        self.code = code
        self.detail = detail


_404 = BaseErrors(code=404, detail="Not found")
