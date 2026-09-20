#!/usr/bin/env python3
"""Backend local da Nai Tiaras.

Implementa uma API pequena, sem dependências externas, usando SQLite.
Para produção, substitua a autenticação de desenvolvimento por um serviço
com sessões seguras, HTTPS e gestão de segredos.
"""

import base64
import hashlib
import json
import mimetypes
import os
import secrets
import sqlite3
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(__file__).resolve().parent / "naitiaras.db"
FRONTEND_ROOT = ROOT / "frontend-naitiaras" if (ROOT / "frontend-naitiaras").exists() else ROOT
FRONTEND_DIST = FRONTEND_ROOT / "dist"
HOST = os.environ.get("NAI_HOST", "127.0.0.1")
PORT = int(os.environ.get("NAI_PORT", "8000"))
ADMIN_EMAIL = os.environ.get("NAI_ADMIN_EMAIL", "admin@naitiaras.com")
ADMIN_PASSWORD = os.environ.get("NAI_ADMIN_PASSWORD", "troque-esta-senha")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
SESSION_TTL_SECONDS = 60 * 60 * 12
ALLOWED_ORIGINS = {item.strip().rstrip("/") for item in os.environ.get("NAI_ALLOWED_ORIGINS", "http://localhost:5173").split(",") if item.strip()}
COOKIE_SECURE = os.environ.get("NAI_COOKIE_SECURE", "0") == "1"
sessions = {}
db_lock = threading.Lock()


def now():
    return datetime.now(timezone.utc).isoformat()


def decimal_money(value):
    try:
        return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("valor monetário inválido")


def token_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return base64.b64encode(salt + digest).decode()


def verify_password(password, encoded):
    raw = base64.b64decode(encoded.encode())
    salt, expected = raw[:16], raw[16:]
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return secrets.compare_digest(actual, expected)


def init_db():
    with get_db() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS admins (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              password_hash TEXT NOT NULL,
              active INTEGER NOT NULL DEFAULT 1,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
              token_hash TEXT PRIMARY KEY,
              admin_id INTEGER NOT NULL REFERENCES admins(id) ON DELETE CASCADE,
              expires_at TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              category TEXT NOT NULL,
              description TEXT NOT NULL DEFAULT '',
              price REAL NOT NULL DEFAULT 0,
              sale_unit TEXT NOT NULL DEFAULT 'unidade',
              stock INTEGER NOT NULL DEFAULT 0,
              image TEXT NOT NULL DEFAULT '',
              status TEXT NOT NULL DEFAULT 'active',
              featured INTEGER NOT NULL DEFAULT 0,
              color TEXT NOT NULL DEFAULT '',
              size TEXT NOT NULL DEFAULT '',
              material TEXT NOT NULL DEFAULT '',
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS orders (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              order_number TEXT UNIQUE NOT NULL,
              customer_name TEXT NOT NULL,
              customer_phone TEXT NOT NULL,
              delivery_method TEXT NOT NULL,
              delivery_address TEXT NOT NULL DEFAULT '',
              delivery_fee REAL NOT NULL DEFAULT 0,
              subtotal REAL NOT NULL,
              total REAL NOT NULL,
              notes TEXT NOT NULL DEFAULT '',
              admin_notes TEXT NOT NULL DEFAULT '',
              stock_deducted INTEGER NOT NULL DEFAULT 0,
              status TEXT NOT NULL DEFAULT 'pending_contact',
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS order_items (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
              product_id INTEGER NOT NULL,
              product_name TEXT NOT NULL,
              sale_unit TEXT NOT NULL,
              unit_price REAL NOT NULL,
              quantity INTEGER NOT NULL,
              subtotal REAL NOT NULL
            );
            """
        )
        columns = {row[1] for row in db.execute("PRAGMA table_info(orders)").fetchall()}
        if "admin_notes" not in columns:
            db.execute("ALTER TABLE orders ADD COLUMN admin_notes TEXT NOT NULL DEFAULT ''")
        if "stock_deducted" not in columns:
            db.execute("ALTER TABLE orders ADD COLUMN stock_deducted INTEGER NOT NULL DEFAULT 0")
        if db.execute("SELECT COUNT(*) FROM admins").fetchone()[0] == 0:
            db.execute(
                "INSERT INTO admins (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                ("Administrador", ADMIN_EMAIL, hash_password(ADMIN_PASSWORD), now()),
            )
        if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            seed = [
                ("Faixas Crochê Coloridas", "Tiras de recém-nascido", "Kit com laços em crochê e meia de seda.", 24.90, "kit", 8, "/assets/produto-1.jpeg", 1),
                ("Laços Gorgurão Sunset", "Laços", "Trio de laços em degradê laranja e amarelo.", 32.90, "kit", 6, "/assets/produto-2.jpeg", 1),
                ("Laços Candy Color", "Laços", "Trio vibrante em tons candy color.", 29.90, "kit", 10, "/assets/produto-3.jpeg", 1),
                ("Faixa Pérola & Corações", "Tiras de recém-nascido", "Delicadeza em tons pastéis com aplique.", 19.90, "unidade", 12, "/assets/produto-4.jpeg", 0),
                ("Laço Duplo Renda Branca", "Laços", "Par de laços delicados para ocasiões especiais.", 22.90, "par", 7, "/assets/produto-5.jpeg", 0),
                ("Tiara Flor Bordada", "Tiaras", "Tiara artesanal com flor bordada à mão.", 34.90, "unidade", 5, "/assets/produto-6.jpeg", 1),
            ]
            db.executemany(
                """INSERT INTO products
                (name, category, description, price, sale_unit, stock, image, featured, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [(*row, now(), now()) for row in seed],
            )


def row_product(row):
    item = dict(row)
    item["featured"] = bool(item["featured"])
    item["price"] = float(item["price"])
    item["available"] = item["status"] == "active" and item["stock"] > 0
    return item


def read_json(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length > 8_000_000:
        raise ValueError("payload muito grande")
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw.decode("utf-8"))


def request_token(handler):
    bearer = handler.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if bearer:
        return bearer
    cookies = handler.headers.get("Cookie", "").split(";")
    for cookie in cookies:
        name, _, value = cookie.strip().partition("=")
        if name == "nai_session":
            return value
    return ""


def authorized(handler):
    token = request_token(handler)
    if not token:
        return False
    with get_db() as db:
        session = db.execute("SELECT expires_at FROM sessions WHERE token_hash = ?", (token_hash(token),)).fetchone()
        if not session:
            return False
        if session["expires_at"] <= now():
            db.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(token),))
            return False
    return True


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")

    def send_json(self, payload, status=200, cookie=None):
        data = json.dumps(payload, ensure_ascii=False).encode()
        origin = self.headers.get("Origin", "").rstrip("/")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Credentials", "true")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_json({"ok": True})

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/products":
                with get_db() as db:
                    rows = db.execute("SELECT * FROM products ORDER BY featured DESC, created_at DESC").fetchall()
                return self.send_json({"products": [row_product(row) for row in rows]})
            if path == "/api/admin/orders":
                if not authorized(self):
                    return self.send_json({"error": "Não autorizado"}, 401)
                with get_db() as db:
                    orders = [dict(row) for row in db.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()]
                return self.send_json({"orders": orders})
            return self.serve_frontend(path)
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 500)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = read_json(self)
            if path == "/api/auth/login":
                with get_db() as db:
                    admin = db.execute("SELECT * FROM admins WHERE email = ? AND active = 1", (body.get("email", ""),)).fetchone()
                if not admin or not verify_password(body.get("password", ""), admin["password_hash"]):
                    return self.send_json({"error": "E-mail ou senha inválidos"}, 401)
                token = secrets.token_urlsafe(32)
                expires_at = datetime.fromtimestamp(datetime.now().timestamp() + SESSION_TTL_SECONDS, timezone.utc).isoformat()
                with get_db() as db:
                    db.execute("INSERT OR REPLACE INTO sessions (token_hash, admin_id, expires_at, created_at) VALUES (?, ?, ?, ?)", (token_hash(token), admin["id"], expires_at, now()))
                secure_flag = "; Secure" if COOKIE_SECURE else ""
                cookie = f"nai_session={token}; Path=/; Max-Age={SESSION_TTL_SECONDS}; HttpOnly; SameSite=Lax{secure_flag}"
                return self.send_json({"admin": {"name": admin["name"], "email": admin["email"]}}, cookie=cookie)
            if path == "/api/auth/logout":
                token = request_token(self)
                with get_db() as db:
                    db.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(token),))
                secure_flag = "; Secure" if COOKIE_SECURE else ""
                return self.send_json({"ok": True}, cookie=f"nai_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax{secure_flag}")
            if path == "/api/orders":
                return self.create_order(body)
            if path == "/api/chat":
                return self.chat(body)
            if path == "/api/admin/products":
                if not authorized(self):
                    return self.send_json({"error": "Não autorizado"}, 401)
                return self.save_product(body)
            return self.send_json({"error": "Rota não encontrada"}, 404)
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 400)

    def do_PATCH(self):
        path = urlparse(self.path).path
        try:
            body = read_json(self)
            if not authorized(self):
                return self.send_json({"error": "Não autorizado"}, 401)
            if path.startswith("/api/admin/products/"):
                product_id = int(path.rsplit("/", 1)[1])
                return self.save_product(body, product_id)
            if path.startswith("/api/admin/orders/"):
                order_id = int(path.rsplit("/", 1)[1])
                return self.update_order(order_id, body)
            return self.send_json({"error": "Rota não encontrada"}, 404)
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 400)

    def update_order(self, order_id, body):
        allowed_statuses = {"pending_contact", "awaiting_confirmation", "confirmed", "preparing", "ready", "completed", "canceled"}
        next_status = body.get("status")
        with get_db() as db:
            db.execute("BEGIN IMMEDIATE")
            order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not order:
                return self.send_json({"error": "Pedido não encontrado"}, 404)
            if next_status is not None and next_status not in allowed_statuses:
                return self.send_json({"error": "Status de pedido inválido"}, 422)
            should_deduct = next_status in {"confirmed", "preparing", "ready", "completed"} and not order["stock_deducted"]
            if should_deduct:
                items = db.execute("SELECT product_id, quantity FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
                for item in items:
                    product = db.execute("SELECT name, stock FROM products WHERE id = ?", (item["product_id"],)).fetchone()
                    if not product or product["stock"] < item["quantity"]:
                        return self.send_json({"error": f"Estoque insuficiente para confirmar {product['name'] if product else 'um produto'}"}, 409)
                for item in items:
                    db.execute("UPDATE products SET stock = stock - ?, updated_at = ? WHERE id = ?", (item["quantity"], now(), item["product_id"]))
                db.execute("UPDATE orders SET stock_deducted = 1 WHERE id = ?", (order_id,))
            db.execute("UPDATE orders SET status = COALESCE(?, status), admin_notes = COALESCE(?, admin_notes), updated_at = ? WHERE id = ?", (next_status, body.get("admin_notes"), now(), order_id))
        return self.send_json({"ok": True, "stock_deducted": bool(should_deduct)})

    def save_product(self, body, product_id=None):
        required = ["name", "category", "price", "sale_unit", "stock"]
        if any(key not in body for key in required):
            return self.send_json({"error": "Preencha nome, categoria, preço, unidade e estoque"}, 422)
        price = decimal_money(body["price"])
        stock = int(body["stock"])
        if price < 0 or stock < 0:
            return self.send_json({"error": "Preço e estoque não podem ser negativos"}, 422)
        values = (
            str(body["name"]).strip()[:160], str(body["category"]).strip()[:80], str(body.get("description", ""))[:2000], float(price),
            body["sale_unit"], stock, body.get("image", ""), int(bool(body.get("featured"))),
            body.get("status", "active"), body.get("color", ""), body.get("size", ""), body.get("material", ""), now()
        )
        with get_db() as db:
            if product_id:
                db.execute(
                    """UPDATE products SET name=?, category=?, description=?, price=?, sale_unit=?, stock=?, image=?, featured=?, status=?, color=?, size=?, material=?, updated_at=? WHERE id=?""",
                    (*values, product_id),
                )
            else:
                db.execute(
                    """INSERT INTO products (name, category, description, price, sale_unit, stock, image, featured, status, color, size, material, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (*values[:-1], now(), values[-1]),
                )
            row = db.execute("SELECT * FROM products WHERE id = ?", (product_id or db.execute("SELECT last_insert_rowid()").fetchone()[0],)).fetchone()
        return self.send_json({"product": row_product(row)})

    def create_order(self, body):
        customer = body.get("customer", {})
        items = body.get("items", [])
        if not customer.get("name") or not customer.get("phone") or not items:
            return self.send_json({"error": "Informe nome, telefone e pelo menos um produto"}, 422)
        if body.get("delivery_method") == "delivery" and not str(body.get("delivery_address", "")).strip():
            return self.send_json({"error": "Informe o endereço para entrega"}, 422)
        with get_db() as db:
            subtotal = Decimal("0.00")
            resolved = []
            for item in items:
                product = db.execute("SELECT * FROM products WHERE id = ? AND status = 'active'", (item.get("id"),)).fetchone()
                try:
                    quantity = int(item.get("quantity", 1))
                except (TypeError, ValueError):
                    return self.send_json({"error": "Quantidade inválida"}, 422)
                if quantity < 1:
                    return self.send_json({"error": "Quantidade inválida"}, 422)
                if not product or product["stock"] < quantity:
                    return self.send_json({"error": "Um dos produtos ficou indisponível. Atualize o carrinho."}, 409)
                line = decimal_money(product["price"]) * quantity
                subtotal += line
                resolved.append((product, quantity, line))
            delivery_fee = Decimal("7.00") if body.get("delivery_method") == "delivery" else Decimal("0.00")
            order_number = f"{datetime.now().strftime('%y%m%d')}-{secrets.randbelow(9000) + 1000}"
            cur = db.execute(
                """INSERT INTO orders (order_number, customer_name, customer_phone, delivery_method, delivery_address, delivery_fee, subtotal, total, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (order_number, str(customer["name"])[:120], str(customer["phone"])[:40], body.get("delivery_method", "pickup"), str(body.get("delivery_address", ""))[:500], float(delivery_fee), float(subtotal), float(subtotal + delivery_fee), str(body.get("notes", ""))[:1000], now(), now()),
            )
            for product, quantity, line in resolved:
                db.execute(
                    "INSERT INTO order_items (order_id, product_id, product_name, sale_unit, unit_price, quantity, subtotal) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (cur.lastrowid, product["id"], product["name"], product["sale_unit"], float(decimal_money(product["price"])), quantity, float(line)),
                )
        return self.send_json({"order_number": order_number, "subtotal": float(subtotal), "delivery_fee": float(delivery_fee), "total": float(subtotal + delivery_fee), "items": [{"name": product["name"], "sale_unit": product["sale_unit"], "unit_price": float(decimal_money(product["price"])), "quantity": quantity, "subtotal": float(line)} for product, quantity, line in resolved]})

    def chat(self, body):
        messages = body.get("messages", [])
        if not isinstance(messages, list) or not messages:
            return self.send_json({"error": "Envie uma mensagem para o atendimento"}, 422)
        messages = [{"role": item.get("role"), "content": str(item.get("content", ""))[:1200]} for item in messages[-10:] if item.get("role") in {"user", "assistant"}]
        with get_db() as db:
            products = [row_product(row) for row in db.execute("SELECT * FROM products WHERE status = 'active' ORDER BY featured DESC, name").fetchall()]
        if not GROQ_API_KEY:
            return self.send_json({"reply": fallback_chat(messages[-1]["content"], products), "provider": "local"})
        catalog = "\n".join(f"- {item['name']} | categoria: {item['category']} | preço: R$ {item['price']:.2f} por {item['sale_unit']} | estoque: {item['stock']}" for item in products)
        system = ("Você é a atendente virtual da Nai Tiaras, loja artesanal de laços, tiaras e tiras de recém-nascido em Recife. "
                  "Responda em português do Brasil, de forma simpática, curta e clara. Nunca invente preços, produtos ou estoque. "
                  f"Se não souber, diga que a equipe pode confirmar pelo WhatsApp {WHATSAPP_NUMBER}. "
                  "A loja fica na R. Adolfo Caminha, 244 - Córrego do Jenipapo, Recife - PE. "
                  "Há retirada na loja e entrega própria a partir de R$ 7,00; o valor final é confirmado pelo WhatsApp. "
                  f"Catálogo atual:\n{catalog}")
        payload = json.dumps({"model": GROQ_MODEL, "messages": [{"role": "system", "content": system}, *messages], "temperature": 0.3, "max_tokens": 300}).encode()
        request = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                result = json.loads(response.read().decode())
            return self.send_json({"reply": result["choices"][0]["message"]["content"], "provider": "groq"})
        except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
            print(f"Falha no chatbot Groq: {exc}")
            return self.send_json({"reply": fallback_chat(messages[-1]["content"], products), "provider": "local"})

    def serve_frontend(self, path):
        target = (FRONTEND_DIST / (path.lstrip("/") or "index.html")).resolve()
        if not str(target).startswith(str(FRONTEND_DIST.resolve())) or not target.exists() or target.is_dir():
            target = FRONTEND_DIST / "index.html"
        if not target.exists():
            return self.send_json({"error": "Frontend não compilado. Execute npm run build."}, 404)
        data = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json", "image/svg+xml"}:
            content_type += "; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

WHATSAPP_NUMBER = "+55 81 98586-4521"


def fallback_chat(question, products):
    text = question.lower()
    if any(word in text for word in ("oi", "olá", "ola", "bom dia", "boa tarde", "boa noite")):
        return "Olá! Sou a assistente da Nai Tiaras. Posso ajudar com produtos, preços, estoque, retirada ou entrega."
    if "entrega" in text:
        return "Temos entrega própria em Recife a partir de R$ 7,00. O valor final depende do endereço e é confirmado pelo WhatsApp. Também é possível retirar na loja, na R. Adolfo Caminha, 244, Córrego do Jenipapo."
    if "retirada" in text or "endereço" in text or "endereco" in text:
        return "A retirada pode ser feita na R. Adolfo Caminha, 244 - Córrego do Jenipapo, Recife - PE."
    if "whatsapp" in text or "comprar" in text or "pedido" in text:
        return "Você pode adicionar os produtos ao carrinho e finalizar pelo WhatsApp. Se preferir, fale conosco pelo número +55 81 98586-4521."
    matches = [item for item in products if item["name"].lower() in text or item["category"].lower() in text]
    if matches:
        return "Encontrei estas opções:\n" + "\n".join(f"• {item['name']}: R$ {item['price']:.2f} por {item['sale_unit']} — {item['stock']} disponíveis" for item in matches[:5])
    return "Posso ajudar a encontrar um produto, consultar preços e disponibilidade ou explicar as opções de retirada e entrega."


if __name__ == "__main__":
    init_db()
    print(f"Nai Tiaras API em http://{HOST}:{PORT}")
    print(f"Login de desenvolvimento: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
