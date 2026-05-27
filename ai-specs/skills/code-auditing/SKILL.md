---
name: code-auditing
description:
  Metodología estructurada en español para realizar auditorías de calidad de código y
  detectar deuda técnica en módulos Odoo.
author: Focuz AI
version: 1.0.0
---

# Skill: Auditoría de Código Odoo (/code-auditing)

Esta skill define la metodología sistemática de 6 fases para evaluar la calidad,
seguridad y mantenibilidad de los módulos Odoo en español.

---

## Fases de la Auditoría

### Fase 0: Setup y Análisis Base

1. Identificar las dependencias del módulo (`__manifest__.py`).
2. Configurar y ejecutar linters locales (`ruff` y `pylint-odoo`) como punto de partida.
3. Cargar la documentación de las dependencias base de Odoo relacionadas.

### Fase 1: Descubrimiento y Mapeo

1. Listar todos los archivos Python, XML (vistas, datos, seguridad), JS (OWL) y SCSS.
2. Agrupar los archivos por funcionalidad (ej. Modelos de facturación, Vistas de
   factura, Wizards de conciliación).

### Fase 2: Análisis Archivo por Archivo

Para cada archivo detectado, analizar:

- **Código Muerto**: Campos declarados no utilizados en vistas, imports no usados,
  métodos deprecados.
- **Antipatrones Odoo**:
  - Uso ineficiente del ORM (queries dentro de bucles `for`).
  - Falta de contexto al llamar métodos del ORM.
  - Sobrescritura de métodos nativos (`write`, `create`) sin llamar a `super()`.
- **Seguridad**:
  - Concatenación de variables en sentencias SQL.
  - Llamadas descontroladas a `.sudo()`.
  - Falta de validación en inputs (`@api.constrains` ausentes).

### Fase 3: Verificación contra Guías de Odoo

1. Validar la estructura según `docs/coding-guidelines.md` (orden de atributos en el
   modelo, nombres de campos, etc.).
2. Comprobar que los mensajes de error e informativos admitan traducción mediante `%`.

### Fase 4: Detección de Patrones Repetidos

1. Identificar código duplicado que pueda abstraerse en un modelo abstracto
   (`models.AbstractModel`) o funciones utilitarias en Python.
2. Identificar inconsistencias en la nomenclatura o en el estilo de las vistas XML.

### Fase 5: Reporte de Resultados

Generar un reporte detallado que contenga:

- Resumen ejecutivo del estado del módulo.
- Detalle de problemas clasificados por prioridad:
  - **Crítico**: Huecos de seguridad (inyección SQL), fallos de transacción.
  - **Alto**: Cuellos de botella en consultas Postgres, herencias XPath inestables.
  - **Medio**: Desviación de directrices de estilo, falta de traducción.
  - **Bajo**: Estilo, comentarios faltantes.
- Plan de acción priorizado para corregir los hallazgos.
