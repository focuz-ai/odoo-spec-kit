# Directrices de Estilo de Código de Odoo (Coding Guidelines)

> [!IMPORTANT] Este documento sintetiza las directrices oficiales de estilo de código de
> Odoo 18.0. Es obligatorio que todos los copilots de IA y agentes de desarrollo sigan
> estas reglas estrictamente para garantizar la legibilidad, mantenimiento y
> extensibilidad de los módulos.

---

## 1. Estructura del Módulo

La organización de archivos de un módulo Odoo debe seguir la estructura estándar:

```text
mi_modulo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── mi_modelo.py
│   └── res_partner.py
├── views/
│   ├── mi_modelo_views.xml
│   └── templates.xml
├── security/
│   ├── ir.model.access.csv
│   └── mi_modelo_security.xml
├── data/
│   └── mi_modelo_data.xml
├── demo/
│   └── mi_modulo_demo.xml
├── wizard/
│   ├── __init__.py
│   ├── mi_wizard.py
│   └── mi_wizard_views.xml
├── report/
│   ├── __init__.py
│   ├── mi_reporte.py
│   └── mi_reporte_views.xml
└── static/
    └── src/
        ├── js/
        ├── xml/
        └── scss/
```

- **Nombres de archivos**: Deben ser descriptivos y reflejar su contenido. Los modelos
  heredados se definen en un archivo con el nombre del modelo base (ej.
  `res_partner.py`). Los archivos XML de vistas deben terminar en `_views.xml`.

---

## 2. Archivos XML

- **Convención de IDs**: Cada XML ID debe tener un prefijo único del módulo. Los nombres
  de vistas deben seguir el patrón: `modelo_view_tipo` (ej. `partner_view_form`).
- **Uso de tags**: Utilizar `<record>` para declarar datos del sistema y vistas.
  Utilizar `<function>` solo cuando sea necesario invocar lógica del backend durante la
  instalación.
- **Acceso sin creación**: Configurar `no_create="1"` en campos Many2one cuando no se
  desee permitir la creación rápida desde la vista, mejorando la integridad de datos.

---

## 3. Desarrollo en Python

- **PEP 8**: Todo el código de Python debe cumplir estrictamente con PEP 8.
- **Orden de Importaciones**:
  1. Bibliotecas estándar de Python (stdlib) (ej. `os`, `re`, `datetime`).
  2. Importaciones de Odoo (ej. `from odoo import models, fields, api, _`).
  3. Importaciones de terceros o locales de Odoo.
- **Formateo de Cadenas**: Utilizar el formateador `%` para cadenas que requieran
  traducción (ej. `_("Error en el registro %s") % record.name`). Para logs y cadenas no
  traducibles, utilizar f-strings o `.format()`.

---

## 4. Orden de Atributos en Modelos

Para mantener la coherencia, declare los componentes dentro de una clase de modelo
Python en este orden estricto:

1. **Atributos Privados**: `_name`, `_description`, `_inherit`, `_inherits`, `_order`,
   `_sql_constraints`.
2. **Métodos por Defecto**: Métodos decorados con `@api.model` que definen defaults (ej.
   `_default_journal_id`).
3. **Declaración de Campos**: Campos estándar, relacionales y computados.
4. **Métodos Computados y de Búsqueda**: `@api.depends`, `@api.depends_context`.
5. **Métodos de Selección**: Métodos que devuelven opciones dinámicas para campos
   `Selection`.
6. **Validaciones y Onchanges**: Métodos decorados con `@api.constrains` y
   `@api.onchange`.
7. **Sobrescrituras de CRUD**: Sobrescribir `create()`, `write()`, `unlink()`.
8. **Métodos de Acción**: Métodos llamados por botones XML (prefijo `action_`).
9. **Métodos de Negocio**: Lógica interna del negocio y cálculos de backend.

---

## 5. Símbolos y Convenciones

- **Nombres de Modelos**: Siempre en singular y con notación de punto (ej.
  `account.move` o `mi_modulo.documento`).
- **Clases**: En PascalCase (ej. `class AccountMove(models.Model):`).
- **Nombres de Campos**: En `snake_case`. Sufijo `_id` para Many2one y `_ids` para
  x2many.
- **Prefijos de Métodos**:
  - Computados: `_compute_nombre_campo`
  - Búsqueda: `_search_nombre_campo`
  - Valor por defecto: `_default_nombre_campo`
  - Validación: `_check_nombre_restriccion`
  - Acciones: `action_nombre_accion`

---

## 6. Programación en Odoo

- **Operaciones de Registro (Recordsets)**: Utilizar siempre los métodos nativos
  `filtered()`, `mapped()` y `sorted()` en lugar de bucles `for` manuales o filtros con
  condicionales cuando sea posible.
- **Propagación del Contexto**: Utilice siempre `with_context()` para pasar información
  a métodos heredados o llamadas internas. **NUNCA** destruya o ignore el contexto
  existente.
- **Control de Transacciones**: **NUNCA** llame a `cr.commit()` manualmente. Odoo
  gestiona las transacciones de forma segura de extremo a extremo. Forzar un commit
  interrumpe las pruebas y corrompe los rollbacks ante errores.
- **Traducciones**: Utilizar `_()` para cadenas traducibles y evitar interpolar
  variables dentro del método de traducción (ej. **CORRECTO**:
  `_("El total no puede ser %s") % total`, **INCORRECTO**:
  `_(f"El total no puede ser {total}")`).

---

## 7. Extensibilidad (Think Extendable)

- **Principio de Responsabilidad Única (SRP)**: Cada clase y método debe tener una única
  responsabilidad clara.
- **Evitar Métodos Monolíticos**: No escriba funciones gigantes. Modularice la lógica
  compleja utilizando métodos gancho pequeños y enfocados:
  - `_prepare_valores_registro(...)` para recopilar datos de creación.
  - `_validate_valores(...)` para validaciones previas.
  - `_do_procesar(...)` para ejecutar la lógica central.
- Esto permite a otros desarrolladores (y a los propios agentes de IA) extender y
  personalizar el comportamiento del módulo heredando métodos específicos con `super()`
  sin necesidad de copiar y pegar código.

---

## 8. JavaScript en el Cliente Web

- ** OWL 2**: Utilizar componentes OWL 2 estructurados.
- **Modo Estricto**: Todo archivo JS debe iniciar con `"use strict";`.
- **Estructura Estática**: Guardar archivos de código de producción en `static/src/` y
  los de pruebas en `static/tests/`.
- **Naming**: Las clases de componentes deben ir en PascalCase.

---

## 9. Hojas de Estilo CSS & SCSS

- **Espacio de Nombres**: Utilizar el prefijo `.o_<modulo>_<nombre>` para todas las
  clases CSS personalizadas para evitar colisiones con el núcleo de Odoo.
- **Evitar `!important`**: No fuerce estilos usando `!important` a menos que sea
  estrictamente necesario para sobreescribir estilos inline de terceros. Utilice la
  especificidad CSS nativa.
- **Variables SCSS**: Integrarse con el sistema de diseño de Odoo utilizando sus
  variables de paleta, espaciado y tipografía oficiales.
