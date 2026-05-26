---
description: Especificación técnica de la API de Odoo 18.0, incluyendo endpoints de JSON-RPC, XML-RPC y la especificación de controladores REST personalizados en español.
alwaysApply: true
---

# Especificación de la API de Odoo 18.0 (API Spec)

Este documento detalla los estándares de integración y comunicación externa con Odoo 18.0. Odoo expone servicios nativos mediante **XML-RPC** y **JSON-RPC**, además de permitir el desarrollo de controladores REST personalizados.

---

## 1. Conectividad Core: XML-RPC / JSON-RPC

El núcleo de Odoo se expone por defecto mediante servicios RPC en el puerto configurado (ej. `8069`).

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

- **Respuesta Exitosa**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "username": "Administrador",
    "uid": 2,
    "session_id": "8c4f923b4ea892fbc1d22",
    "company_id": 1
  }
}
```

---

### B. Llamada General a Métodos ORM (`/web/dataset/call_kw`)
Una vez autenticado, puede ejecutar cualquier método de un modelo ORM (ej. `search_read`, `create`, `write`, `action_post`).

- **Método**: `POST`
- **Ruta**: `/web/dataset/call_kw`
- **Payload**:
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

## 2. API REST Personalizada (Controladores en Python)

Para integraciones móviles o con plataformas de terceros donde se requiere una API REST JSON limpia, se configuran controladores en Odoo heredando de `http.Controller`.

### Ruta 1: Obtener Facturas de Clientes
- **Método HTTP**: `GET`
- **Ruta**: `/api/v1/facturas`
- **Autenticación**: Token de API en cabecera (`X-API-Key`) o Sesión de Odoo.
- **Parámetros de consulta (Query)**:
  - `limit` (opcional, entero): Número de registros a retornar (default: 20).
  - `state` (opcional, selección): Estado de la factura (`draft`, `posted`).

- **Ejemplo de Respuesta (200 OK)**:
```json
{
  "status": "success",
  "data": [
    {
      "id": 154,
      "nombre": "INV/2026/05/0001",
      "fecha_factura": "2026-05-26",
      "cliente": "Cliente de Prueba S.A.",
      "total": 1160.00,
      "moneda": "MXN",
      "estado": "posted"
    }
  ]
}
```

---

### Ruta 2: Crear Factura de Cliente (Borrador)
Crea una nueva cabecera de factura en estado borrador.

- **Método HTTP**: `POST`
- **Ruta**: `/api/v1/facturas`
- **Autenticación**: Requerida.
- **Payload**:
```json
{
  "cliente_id": 45,
  "fecha_factura": "2026-05-26",
  "lineas": [
    {
      "producto_id": 12,
      "cantidad": 2,
      "precio_unitario": 500.00,
      "impuesto_ids": [1]
    }
  ]
}
```

- **Respuesta de Creación exitosa (201 Created)**:
```json
{
  "status": "created",
  "factura_id": 155,
  "nombre": "INV/2026/05/0002",
  "estado": "draft"
}
```

- **Errores de Validación Comunes (400 Bad Request)**:
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "El cliente seleccionado no existe o no tiene una compañía asociada válida."
}
```

---

## 3. Códigos de Estado y Manejo de Errores

La API REST personalizada debe responder utilizando códigos de estado HTTP estándar:

| Código HTTP | Significado | Causa Común en Odoo |
|---|---|---|
| **`200 OK`** | Operación exitosa | Lectura o actualización exitosa de registros. |
| **`201 Created`** | Registro creado | Creación exitosa de una factura u objeto. |
| **`400 Bad Request`** | Error en los parámetros | JSON mal formado o tipos de datos inválidos en el payload. |
| **`401 Unauthorized`**| Falta autenticación | Falta la cookie de sesión o el header `X-API-Key`. |
| **`403 Forbidden`** | Sin privilegios | El usuario autenticado no pertenece al grupo de seguridad requerido en Odoo. |
| **`404 Not Found`** | Recurso no encontrado | El ID de registro especificado no existe en la base de datos. |
| **`500 Internal Error`**| Fallo del servidor | Error inesperado en el código de Python (ej. `ZeroDivisionError`). |
