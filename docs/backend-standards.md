# Estándares de Desarrollo Backend y Vistas XML en Odoo 18.0 (Backend Standards)

> [!IMPORTANT]
> Este documento rige todas las decisiones de diseño técnico, estructura y codificación del backend y las vistas XML del proyecto. Todos los agentes de IA deben utilizarlo como la guía maestra de estándares backend.

---

## 1. Stack Tecnológico

- **Lenguaje**: Python 3.11+
- **Plataforma**: Odoo 18.0 (Community y Enterprise)
- **Base de Datos**: PostgreSQL 15+
- **API**: JSON-RPC 2.0 y XML-RPC para integraciones externas.

---

## 2. Patrones de Modelos de Odoo (ORM)

Odoo cuenta con tres clases base fundamentales para la persistencia de datos:

- **`models.Model`**: Modelos persistentes estándar (se mapean a tablas de PostgreSQL).
- **`models.TransientModel`**: Modelos temporales para Wizards. Se limpian periódicamente de la base de datos de forma automática.
- **`models.AbstractModel`**: Modelos abstractos que no tienen tabla física propia, pero sirven para heredar campos y comportamientos a múltiples modelos.

### Buenas Prácticas y Patrones de Odoo 18.0:
- **Decorador `@api.model_create_multi`**: Obligatorio en todos los métodos `create(self, vals_list)`. Este decorador permite que Odoo procese la creación de registros en lotes eficientes (batching), reduciendo el número de queries `INSERT`.
- **Atributo `precompute=True`**: Utilizar en campos computados almacenados (`store=True`) que se necesiten calcular antes de escribir el registro en la base de datos (evitando una query `UPDATE` posterior).
- **Atributo `check_company=True`**: Obligatorio en todos los campos relacionales (`Many2one`, `Many2many`, `One2many`) que involucren modelos multi-compañía para forzar la restricción del entorno (evita que un usuario asocie un registro de la Compañía A con uno de la Compañía B).

```python
from odoo import models, fields, api, _

class FacturaLocal(models.Model):
    _name = 'factura.local'
    _description = 'Factura Contable Localizada'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Referencia', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True, check_company=True)
    
    # Campo computado almacenado y pre-calculado
    monto_total = fields.Monetary(string='Total', compute='_compute_monto_total', store=True, precompute=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.depends('partner_id')
    def _compute_monto_total(self):
        for record in self:
            # Lógica del cálculo
            record.monto_total = 100.0

    @api.model_create_multi
    def create(self, vals_list):
        # Implementación por lotes
        return super().create(vals_list)
```

---

## 3. Patrones de Herencia de Modelos

Odoo soporta tres tipos principales de herencia:

- **Herencia Clásica (Extensión de Modelo)**:
  `_inherit = 'res.partner'`
  Agrega campos o métodos a un modelo existente sin cambiar su tabla o su nombre técnico.
- **Herencia por Delegación**:
  `_inherits = {'res.partner': 'partner_id'}`
  Mapea un registro hijo a uno padre automáticamente creando una relación One2one física en base de datos.
- **Herencia por Clonación (Polimorfismo de Prototipo)**:
  `_name = 'nuevo.partner'`
  `_inherit = 'res.partner'`
  Crea una nueva tabla física (`nuevo.partner`) que clona todos los campos y la lógica del modelo heredado (`res.partner`).

---

## 4. Mejores Prácticas del ORM

- **Uso del Helper `Command`**: Para manipular campos relacionales x2many (`One2many`, `Many2many`), es obligatorio utilizar la clase `Command` en lugar de tuplas crudas:
  - `Command.create(vals)` equivalente a `(0, 0, vals)`
  - `Command.update(id, vals)` equivalente a `(1, id, vals)`
  - `Command.delete(id)` equivalente a `(2, id, 0)` (borrar de base de datos)
  - `Command.unlink(id)` equivalente a `(3, id, 0)` (quitar relación)
  - `Command.link(id)` equivalente a `(4, id, 0)` (asociar existente)
  - `Command.clear()` equivalente a `(5, 0, 0)` (limpiar todas las relaciones)
  - `Command.set(ids)` equivalente a `(6, 0, ids)` (reemplazar por lista)
- **Evitar N+1 y queries ineficientes**: Utilizar `filtered()`, `mapped()` y `sorted()` sobre recordsets cargados. Si se requiere agrupar datos, usar `read_group()` para que la agregación la haga PostgreSQL.
- **Propagación del Contexto**: Pasar siempre el contexto al llamar métodos del ORM (ej. `self.with_context(mi_contexto).write(...)`).

---

## 5. Seguridad Estricta (ACLs, Rules, SQL)

- **`ir.model.access.csv`**: Todo modelo debe estar declarado en este archivo con permisos de lectura, escritura, creación y eliminación para los grupos correspondientes.
- **Record Rules (XML)**: Utilizar record rules con `domain_force` para restringir el acceso a nivel de fila (multi-compañía, multi-sucursal).
- **Prevención de Inyección SQL**: **NUNCA** construya consultas crudas concatenando o formateando variables (`f"SELECT ... WHERE id = {mi_id}"`). Es obligatorio utilizar la clase `odoo.tools.SQL`:
```python
from odoo.tools import SQL

# CORRECTO
self.env.cr.execute(SQL("SELECT name FROM res_partner WHERE id = %s", partner_id))

# CORRECTO (Usando SQL composition de Odoo 18.0)
query = SQL("SELECT name FROM res_partner")
if partner_id:
    query = SQL("%s WHERE id = %s", query, partner_id)
self.env.cr.execute(query)
```
- **Uso de `sudo()`**: Limitar el uso de `sudo()` únicamente para omitir validaciones de acceso en operaciones de sistema controladas. Inmediatamente después de `sudo()`, use `with_user()` para volver a limitar privilegios si es necesario.

---

## 6. Patrones de Vistas XML Declarativas

Las vistas XML de Odoo deben ser limpias y usar herencia mediante expresiones `xpath` precisas.

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Vista Form estándar -->
    <record id="factura_local_view_form" model="ir.ui.view">
        <field name="name">factura.local.view.form</field>
        <field name="model">factura.local</field>
        <field name="arch" type="xml">
            <form string="Factura Local">
                <header>
                    <button name="action_aprobar" string="Aprobar" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,open,close"/>
                </header>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="partner_id" no_create="1"/>
                        </group>
                        <group>
                            <field name="company_id" groups="base.group_multi_company"/>
                            <field name="monto_total"/>
                        </group>
                    </group>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Vista de lista / Tree -->
    <record id="factura_local_view_list" model="ir.ui.view">
        <field name="name">factura.local.view.list</field>
        <field name="model">factura.local</field>
        <field name="arch" type="xml">
            <list string="Facturas Locales">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="monto_total" sum="Total General"/>
                <field name="state"/>
            </list>
        </field>
    </record>
</odoo>
```

---

## 7. Controladores Web (`controllers/`)

- Utilizar el decorador `@http.route()` especificando la autenticación requerida (`auth='user'`, `auth='public'` o `auth='none'`).
- Tipo de ruta: `type='json'` para peticiones RPC del cliente web, `type='http'` para peticiones web tradicionales/APIs externas.
- **Validación**: Validar de manera estricta todos los parámetros de entrada y lanzar excepciones correspondientes si no se cumplen las condiciones.

---

## 8. Wizards (`TransientModel`) y Reportes

- **Wizards**: Utilizar siempre clases que heredan de `models.TransientModel` para recopilar datos de entrada temporales antes de realizar acciones en lote.
- **Reportes**: Declarar reportes QWeb XML utilizando `ir.actions.report`. La lógica de generación y el formato del papel deben estar detallados bajo este registro.

---

## 9. Framework de Pruebas (Testing)

Odoo proporciona clases de prueba específicas adaptadas al ciclo de transacciones de base de datos. Todas las clases de prueba se guardan en el subdirectorio `tests/` y se importan explícitamente en `tests/__init__.py`.

- **`odoo.tests.TransactionCase`**: Es la clase recomendada. Cada método de prueba corre en una subtransacción con un `savepoint` PostgreSQL que se revierte de forma automática al finalizar. Se debe utilizar el método de clase `setUpClass()` para crear los datos maestros comunes una sola vez, optimizando la velocidad del test.
- **`odoo.tests.SingleTransactionCase`**: Ejecuta todos los métodos secuencialmente en una única transacción de base de datos que se revierte al finalizar la última prueba. Útil para flujos continuos.
- **`odoo.tests.HttpCase`**: Proporciona soporte para peticiones HTTP y simulación de interfaz mediante tours con un navegador Chrome Headless. Permite depurar localmente con los parámetros `watch=True` o `debug=True`.
- **Uso de Etiquetas (`@tagged`)**: Utilizar para clasificar la ejecución (ej. `@tagged('post_install', '-at_install')`). Las etiquetas aplican únicamente a clases.
- **Tests de Integración (Tours)**: Los tours JavaScript se guardan en `static/tests/tours/` y se registran en `web.assets_tests`. En Python, se disparan con `self.start_tour()`.
