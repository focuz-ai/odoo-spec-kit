---
name: odoo-scaffold
description:
  Use esta skill cuando necesite inicializar la estructura de carpetas y archivos base
  de un nuevo módulo o addon para Odoo 16.0.
author: Focuz AI
version: 1.0.0
---

# Skill: Scaffolding de Módulos Odoo (/odoo-scaffold)

Esta skill define la automatización del andamiaje (scaffold) para crear módulos Odoo
robustos y alineados con las directrices de `docs/coding-guidelines.md`.

---

## Estructura de Directorios a Generar

El agente debe crear la siguiente jerarquía física de archivos al inicializar un módulo:

```text
mi_modulo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
├── views/
├── security/
│   ├── ir.model.access.csv
├── data/
├── tests/
│   ├── __init__.py
└── static/
    └── src/
        ├── js/
        ├── xml/
        └── scss/
```

---

## Contenido de Archivos Plantilla (Español)

### 1. `__manifest__.py`

El manifiesto debe incluir los metadatos y bundles vacíos iniciales:

```python
# -*- coding: utf-8 -*-
{
    'name': 'Nombre del Módulo en Español',
    'summary': 'Resumen de la funcionalidad del módulo',
    'description': """
Descripción detallada de los objetivos y alcance del módulo.
    """,
    'author': 'Focuz AI',
    'website': 'https://focuz.ai',
    'category': 'Accounting',  # Foco inicial
    'version': '16.0.1.0.0',
    'depends': ['base', 'account'],  # Dependencias contables por defecto
    'data': [
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'mi_modulo/static/src/js/**/*.js',
            'mi_modulo/static/src/xml/**/*.xml',
            'mi_modulo/static/src/scss/**/*.scss',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### 2. `security/ir.model.access.csv`

Encabezado estándar de ACLs de Odoo:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

### 3. Archivos `__init__.py`

- Raíz:
  ```python
  # -*- coding: utf-8 -*-
  from . import models
  ```
- En `models/`:
  ```python
  # -*- coding: utf-8 -*-
  # from . import mi_modelo
  ```

---

## Instrucciones del Proceso

1. Solicitar al usuario el **nombre técnico** del módulo (ej. `account_local_invoice`).
2. Crear recursivamente todos los directorios descritos en la sección 1.
3. Escribir los archivos de plantilla con los metadatos correspondientes en español.
4. Mostrar en consola el árbol de archivos creado para su confirmación.
