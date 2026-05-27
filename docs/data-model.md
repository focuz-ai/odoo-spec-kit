---
description: Documentación y ejemplo del modelo de datos de Contabilidad (Accounting) en Odoo 16.0, detallando las entidades principales, campos clave, reglas relacionales y diagrama ER.
alwaysApply: true
---

# Modelo de Datos: Contabilidad en Odoo 16.0 (Data Model)

Este documento detalla la arquitectura de base de datos y modelos del módulo de Contabilidad (`account`) de Odoo 16.0, sirviendo de referencia de diseño técnico para la creación o extensión de módulos contables.

---

## 1. Descripción de Modelos Core

En Odoo, un asiento contable y una factura (de cliente o proveedor) comparten la misma tabla física (`account.move`). La diferencia radica en el tipo de asiento definido por el campo `move_type`.

### A. Asiento / Factura Contable (`account.move`)
Representa la cabecera de un diario contable, una factura de cliente, factura rectificativa o una factura de proveedor.

**Campos Clave:**
- `id` (`integer`): Identificador único (Primary Key).
- `name` (`char`): Secuencia o número único del asiento (ej. `INV/2026/05/0001` o `MISC/2026/001`).
- `move_type` (`selection`): Tipo de asiento. Valores comunes:
  - `entry`: Asiento contable manual (Journal Entry).
  - `out_invoice`: Factura de cliente.
  - `out_refund`: Factura rectificativa de cliente (Nota de Crédito).
  - `in_invoice`: Factura de proveedor.
  - `in_refund`: Factura rectificativa de proveedor.
- `state` (`selection`): Estado del asiento (`draft`, `posted`, `cancel`).
- `date` (`date`): Fecha contable del asiento.
- `invoice_date` (`date`): Fecha de emisión de la factura (solo para facturas).
- `partner_id` (`many2one`): Referencia al cliente o proveedor (`res.partner`).
- `journal_id` (`many2one`): Diario en el que se registra (`account.journal`).
- `company_id` (`many2one`): Compañía dueña del registro (obligatorio, `check_company=True`).
- `line_ids` (`one2many`): Líneas de asiento contable de contrapartida (`account.move.line`).
- `invoice_line_ids` (`one2many`): Líneas detalladas de la factura comercial.

---

### B. Línea de Asiento Contable (`account.move.line`)
Representa los apuntes contables individuales (débitos y créditos) asociados a un asiento. Se rige por el principio de partida doble (la suma de débitos debe ser igual a la de créditos).

**Campos Clave:**
- `id` (`integer`): Identificador único.
- `move_id` (`many2one`): Asiento padre al que pertenece (`account.move`, cascada `ondelete='cascade'`).
- `account_id` (`many2one`): Cuenta contable asociada (`account.account`, obligatorio, `check_company=True`).
- `partner_id` (`many2one`): Contacto asociado.
- `name` (`char`): Etiqueta o glosa de la línea.
- `debit` (`monetary`): Monto en el Debe.
- `credit` (`monetary`): Monto en el Haber.
- `balance` (`monetary`): Balance neto (`debit - credit`). Computado y almacenado.
- `amount_currency` (`monetary`): Monto expresado en la moneda original de la transacción.
- `currency_id` (`many2one`): Moneda de la línea (si difiere de la de la compañía).
- `tax_ids` (`many2many`): Impuestos aplicados a esta línea (`account.tax`).

---

### C. Cuenta Contable (`account.account`)
Define la estructura del Plan de Cuentas (Chart of Accounts).

**Campos Clave:**
- `code` (`char`): Código numérico/alfanumérico único (ej. `101000` para Caja).
- `name` (`char`): Nombre de la cuenta (ej. `Caja General`).
- `account_type` (`selection`): Tipo de cuenta (ej. `asset_receivable`, `liability_payable`, `income`, `expense`).
- `reconcile` (`boolean`): Define si la cuenta permite conciliación (ej. clientes y proveedores).
- `company_id` (`many2one`): Compañía dueña de la cuenta.

---

### D. Diario Contable (`account.journal`)
Utilizado para agrupar transacciones del mismo tipo.

**Campos Clave:**
- `name` (`char`): Nombre del diario (ej. `Facturas de Clientes`).
- `code` (`char`): Código corto para las secuencias (ej. `INV`).
- `type` (`selection`): Tipo de diario (`sale`, `purchase`, `cash`, `bank`, `general`).
- `default_account_id` (`many2one`): Cuenta contable por defecto del diario.

---

### E. Impuestos (`account.tax`)
Define el cálculo de impuestos (IVA, retenciones, etc.) aplicables a las líneas de ventas o compras.

**Campos Clave:**
- `name` (`char`): Nombre descriptivo (ej. `IVA 16% Ventas`).
- `amount_type` (`selection`): Tipo de cálculo (`percent`, `division`, `fixed`).
- `amount` (`float`): Porcentaje o monto fijo del impuesto.
- `type_tax_use` (`selection`): Dónde se aplica (`sale`, `purchase`, `none`).

---

## 2. Diagrama de Entidad-Relación (ERD)

El siguiente diagrama representa cómo se vinculan los modelos de contabilidad en Odoo 16.0:

```mermaid
erDiagram
    account_journal {
        integer id PK
        string name
        string code
        string type
        integer default_account_id FK
        integer company_id FK
    }
    
    account_account {
        integer id PK
        string code
        string name
        string account_type
        boolean reconcile
        integer company_id FK
    }

    account_move {
        integer id PK
        string name
        string move_type
        string state
        date date
        date invoice_date
        integer partner_id FK
        integer journal_id FK
        integer company_id FK
    }

    account_move_line {
        integer id PK
        integer move_id FK
        integer account_id FK
        integer partner_id FK
        string name
        monetary debit
        monetary credit
        monetary balance
        monetary amount_currency
        integer currency_id FK
    }

    account_tax {
        integer id PK
        string name
        string amount_type
        float amount
        string type_tax_use
        integer company_id FK
    }

    account_payment {
        integer id PK
        string name
        string payment_type
        monetary amount
        integer journal_id FK
        integer move_id FK
        integer company_id FK
    }

    ;; Relaciones entre entidades
    account_journal ||--o{ account_move : "registra"
    account_account ||--o{ account_journal : "cuenta_por_defecto"
    account_account ||--o{ account_move_line : "apunta_a"
    
    account_move ||--|{ account_move_line : "contiene"
    account_move_line }o--o{ account_tax : "aplica"
    
    account_payment ||--o| account_move : "crea_asiento"
    account_journal ||--o{ account_payment : "metodo_pago"
```

---

## 3. Principios Clave de Diseño y Restricciones

1. **Partida Doble Obligatoria**:
   Al crear o modificar líneas de un asiento contable (`account.move.line`), el sistema verifica mediante restricciones de base de datos y métodos ORM que la suma del Debe sea igual a la suma del Haber (`sum(debit) == sum(credit)`). Si esto no se cumple, el asiento no puede pasar del estado `draft` a `posted`.

2. **Multicompañía Estricto**:
   Odoo 16.0 valida rigurosamente los accesos multicompañía. Los campos `company_id` actúan como filtros duros. No se pueden mezclar líneas de asientos contables apuntando a cuentas de una Compañía A en un asiento perteneciente a la Compañía B.

3. **Cuentas por Tipo**:
   El campo `account_type` en `account.account` define el comportamiento contable. Por ejemplo, las líneas de facturas de clientes solo pueden apuntar a cuentas del tipo `asset_receivable`, y las de proveedores a `liability_payable`.
