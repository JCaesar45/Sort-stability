# ✦ AURUM

> Six objects. One storefront. Zero dependencies.

AURUM is a small luxury storefront built to show how a few honest layers fit together: a single-file front end, a standard-library Python API, a typed TypeScript catalog module, and a Java order validator.

## Product structure

```
sort-stability/
├── public/
│   └── index.html          HTML + CSS + JavaScript in one file
├── data/
│   └── products.json       Catalog served by the API
├── src/
│   └── catalog.ts          Typed sort, filter and total helpers
├── java/
│   └── OrderValidator.java Subtotal, tax and email validation
├── server.py               Static hosting + /api/products + /api/orders
└── README.md
```

## Run it

```bash
python3 server.py                        # http://localhost:8000
java java/OrderValidator.java            # Java 16+
npx tsc --target es2020 --strict src/catalog.ts
```

Opened without the server, the page falls back to its built-in catalog and confirms orders in demo mode.

## Design notes

- **Stable sorting.** Products with equal prices must keep their catalog order, so every sort carries the original index as a tie-breaker. The same logic lives in the page and in `catalog.ts`.
- **Server-side pricing.** The API recomputes totals from `products.json` and ignores any client-sent price.
- **No dependencies.** Python uses only `http.server`, Java runs as a single-file program, and the page loads nothing external.
- **Motion with restraint.** Reveal animations use `IntersectionObserver`, and the particle field respects `prefers-reduced-motion`.

## API

| Method | Path | Body | Response |
|--------|------|------|----------|
| GET | `/api/products` | none | array of products |
| POST | `/api/orders` | `{"email": "...", "items": [{"id": 1, "qty": 2}]}` | `201 {"orderId", "total"}` or `400` |

## References

MDN Web Docs. (n.d.). *Intersection Observer API*. Mozilla. https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API

Microsoft. (n.d.). *TypeScript documentation*. https://www.typescriptlang.org/docs/

OpenJDK. (2018). *JEP 330: Launch single-file source-code programs*. https://openjdk.org/jeps/330

Python Software Foundation. (n.d.). *http.server — HTTP servers*. Python 3 documentation. https://docs.python.org/3/library/http.server.html
