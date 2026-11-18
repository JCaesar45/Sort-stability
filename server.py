import json
import os
import re
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

with open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8") as fh:
    PRODUCTS = json.load(fh)
BY_ID = {p["id"]: p for p in PRODUCTS}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC, **kwargs)

    def reply(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/products":
            return self.reply(200, PRODUCTS)
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/orders":
            return self.reply(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            email = str(data["email"])
            items = data["items"]
            if not EMAIL.match(email) or not isinstance(items, list) or not items:
                raise ValueError
            total = 0
            for item in items:
                product = BY_ID[item["id"]]
                qty = item["qty"]
                if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
                    raise ValueError
                total += product["price"] * qty
        except (ValueError, KeyError, TypeError):
            return self.reply(400, {"error": "invalid order"})
        return self.reply(201, {"orderId": uuid.uuid4().hex[:10].upper(), "total": total})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"AURUM running on http://localhost:{port}")
    ThreadingHTTPServer(("", port), Handler).serve_forever()
