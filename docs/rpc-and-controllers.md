---
description:
  Documentación técnica sobre cómo exponer y consumir servicios en Odoo utilizando los protocolos nativos XML-RPC / JSON-RPC y Controladores HTTP/Web personalizados.
alwaysApply: true
---

# Integración y Controladores (RPC & Controllers)

Este documento detalla los estándares de integración y comunicación externa con Odoo.
A diferencia de aplicaciones basadas en REST o API-first (como NodeJS con OpenAPI), **Odoo expone su núcleo por defecto mediante XML-RPC y JSON-RPC**. La creación de APIs REST tradicionales debe ser la excepción, no la regla.

---

## 1. Conectividad Core: XML-RPC / JSON-RPC

El ORM de Odoo se expone por defecto. Cualquier sistema externo que necesite interactuar con Odoo debe utilizar preferiblemente estos protocolos nativos.

### A. Autenticación (`/web/session/authenticate`)

Para consumir los servicios mediante JSON-RPC, primero se debe obtener una sesión web.

- **Método**: `POST`
- **Ruta**: `/web/session/authenticate`
- **Cabecera**: `Content-Type: application/json`
- **Payload (JSON-RPC 2.0)**:

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "db": "mi_base_datos",
    "login": "admin@empresa.com",
    "password": "mi_password_segura"
  }
}
```

### B. Llamada General a Métodos ORM (`/web/dataset/call_kw`)

Una vez autenticado, puede ejecutar cualquier método de un modelo ORM (ej.
`search_read`, `create`, `write`, `action_post`).

- **Ruta**: `/web/dataset/call_kw`
- **Ejemplo**:

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "model": "account.move",
    "method": "search_read",
    "args": [[["move_type", "=", "out_invoice"]]],
    "kwargs": {
      "fields": ["name", "invoice_date", "amount_total"],
      "limit": 5
    }
  }
}
```

---

## 2. Controladores Web Personalizados (`http.Controller`)

Si la integración requiere webhooks (donde un sistema externo nos llama a nosotros de manera asíncrona) o un payload JSON estricto que no se ajusta a JSON-RPC, debemos declarar Controladores Personalizados en Odoo.

### Reglas de Diseño de Controladores:

1. **Ubicación:** Todo controlador debe ubicarse en la carpeta `/controllers/` y registrarse en `__init__.py`.
2. **Autenticación Estricta (`auth=`)**:
   - `auth='user'`: Requiere que el usuario esté logueado (sesión activa).
   - `auth='public'`: Accesible para cualquier visitante no autenticado (peligroso, usar con cuidado extremo).
   - `auth='none'`: Salta el chequeo de base de datos. Útil para endpoints muy genéricos.
3. **Tipo de Respuesta (`type=`)**:
   - `type='json'`: Para llamadas donde Odoo envolverá la respuesta en un JSON-RPC format.
   - `type='http'`: Para endpoints web convencionales, descarga de archivos o webhooks limpios (REST manual).

### Ejemplo: Controlador Webhook HTTP (REST-like)

```python
from odoo import http
from odoo.http import request
import json

class FacturaController(http.Controller):

    @http.route('/api/v1/facturas', type='http', auth='user', methods=['GET'], csrf=False)
    def obtener_facturas(self, **kwargs):
        # La autenticación ya está garantizada por auth='user'
        facturas = request.env['account.move'].search([('move_type', '=', 'out_invoice')])
        data = []
        for fac in facturas:
            data.append({
                'id': fac.id,
                'nombre': fac.name,
                'total': fac.amount_total
            })
            
        return request.make_response(
            json.dumps({'status': 'success', 'data': data}),
            headers=[('Content-Type', 'application/json')]
        )
```

### Ejemplo: Endpoint para JSON-RPC Interno de Frontend (OWL)

```python
class FrontendController(http.Controller):

    @http.route('/mi_modulo/obtener_datos', type='json', auth='user')
    def obtener_datos(self, parametro_x):
        # Odoo se encarga de serializar el return a JSON automáticamente
        return {'resultado': parametro_x * 2}
```

---

## 3. Códigos de Estado HTTP y Errores (para Controladores `type='http'`)

Si diseña una API manual vía `type='http'`, respete el estándar HTTP:

| Código HTTP              | Causa Común en Odoo                                                          |
| ------------------------ | ---------------------------------------------------------------------------- |
| **`200 OK`**             | Lectura o actualización exitosa de registros.                                |
| **`201 Created`**        | Creación exitosa de un registro.                                             |
| **`400 Bad Request`**    | JSON mal formado o tipos de datos inválidos en el payload (`kwargs`).        |
| **`401 Unauthorized`**   | Falta la cookie de sesión o el header de API Key.                            |
| **`403 Forbidden`**      | El usuario autenticado no pertenece al grupo de seguridad requerido (ACL).   |
| **`404 Not Found`**      | El ID de registro especificado no existe en la base de datos.                |
| **`500 Internal Error`** | Excepciones no capturadas de Python o error en base de datos.                |
