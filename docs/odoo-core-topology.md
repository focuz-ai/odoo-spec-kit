---
description:
  Cheat sheet de la Topología Core de Odoo. Contiene las reglas inquebrantables de los modelos base para evitar alucinaciones de IA y la recomendación de introspección dinámica vía MCP.
alwaysApply: true
---

# Topología Core y Anti-Alucinaciones de Odoo

Odoo es un ERP masivo. Para evitar que la IA alucine tablas, modelos o relaciones que no existen, respeta **estrictamente** las siguientes reglas arquitectónicas:

## 1. El Glosario de Modelos Inquebrantables (Core Entities)

- **Contactos, Clientes y Proveedores**: NUNCA inventes modelos como `crm.customer` o `res.vendor`. Todo actor externo o interno es un **`res.partner`**.
- **Productos**: 
  - `product.template`: Plantilla genérica del producto (ej. "Camiseta").
  - `product.product`: La variante específica que maneja stock (ej. "Camiseta Roja Talla M").
- **Ventas (Sales)**: `sale.order` (Cabecera) y `sale.order.line` (Líneas). Importante: Confirmar una venta NO rebaja inventario mágicamente, esto dispara un Albarán de entrega.
- **Inventario (Stock)**: `stock.picking` (Albaranes/Transferencias) y `stock.move` (Movimientos de stock).
- **Facturación y Contabilidad**: NUNCA uses `account.invoice` (deprecado en Odoo 13+). Toda factura, nota de crédito o asiento de diario es un **`account.move`** (Cabecera) con sus respectivos **`account.move.line`**.
- **Recursos Humanos**: `hr.employee` (Empleados) y `hr.contract` (Contratos).

## 2. Introspección Dinámica de Base de Datos (Vía MCP)

Dado que Odoo permite personalizaciones infinitas (campos `x_studio_` o módulos de terceros), es imposible documentar todos los campos estáticamente.

> [!IMPORTANT]
> **Introspección con MCP**: Se recomienda encarecidamente a los agentes de IA que, si el servidor `mcp-server-odoo` está configurado y disponible en el entorno del usuario, utilicen el recurso `odoo://{model}/fields` para leer el esquema real de la base de datos **antes** de proponer campos nuevos o modificaciones.

Si el MCP no está disponible, asume el esquema estándar de Odoo y documenta cualquier campo nuevo necesario en la especificación técnica para que el desarrollador lo implemente.
