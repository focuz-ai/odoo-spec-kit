# Metodología de Detección de Código Muerto (Odoo 16.0)

Guía para detectar código no utilizado en addons Odoo minimizando falsos positivos.

## Objetivo

Reducir deuda técnica y complejidad eliminando artefactos no usados sin romper puntos de
entrada dinámicos de Odoo.

## Alcance de código muerto

1. Importaciones no usadas en Python/JS.
2. Variables, funciones y métodos no referenciados.
3. Archivos huérfanos (`models`, `views`, `static`, `tests`) fuera de carga real.
4. XML IDs y registros de datos sin uso.
5. Assets declarados y nunca consumidos (o consumidos y no declarados).

## Fuentes de verdad en Odoo

Antes de marcar como muerto, verificar referencias en:

- `__manifest__.py` (`depends`, `data`, `assets`, `demo`).
- `__init__.py` de paquete y subpaquetes.
- Herencias de modelos (`_inherit`, `_name`, `_inherits`).
- Vistas XML (`record`, `menuitem`, `act_window`, `report`, `template`).
- Llamadas indirectas por nombre de método desde botones XML (`type="object"`).
- Registro de componentes/servicios en OWL (`registry.category(...).add(...)`).

## Flujo recomendado

### 1. Descubrimiento inicial

- Listar archivos Python/XML/JS/SCSS por addon.
- Detectar importaciones y símbolos aparentemente no usados con herramientas disponibles
  (`ruff`, búsqueda textual, revisión manual).

### 2. Verificación de falsos positivos

Para cada candidato, validar:

1. Referencias dinámicas por strings (`env[model_name]`, nombres de métodos en XML,
   registry frontend).
2. Carga por manifest aunque no exista import directo.
3. Uso por herencia o extensión de terceros.
4. Uso solo en pruebas o solo en demo data.
5. Uso por hooks de instalación/migración.

### 3. Clasificación

- **Verificado como muerto**: sin referencias estáticas ni dinámicas válidas.
- **Sospechoso**: evidencia incompleta, requiere validación funcional.
- **Falso positivo**: hay referencia dinámica o contractual.

### 4. Remoción segura

1. Eliminar en cambios pequeños y atómicos.
2. Actualizar `__init__.py`, `__manifest__.py`, XML IDs y assets relacionados.
3. Ejecutar validaciones disponibles (`pre-commit`, tests del módulo si están
   disponibles).
4. Confirmar que no se rompan vistas, acciones ni carga del addon.

## Checklist de validación por tipo

### Python

- [ ] ¿El método se invoca desde botón XML (`type="object"`)?
- [ ] ¿El modelo se usa por `_inherit` o por nombre técnico en otros addons?
- [ ] ¿El archivo está importado en `__init__.py`?

### XML

- [ ] ¿El archivo está listado en `__manifest__.py:data`?
- [ ] ¿El XML ID es referenciado por menús/acciones/reportes/seguridad?
- [ ] ¿El `xpath` extiende una vista activa?

### Frontend (JS/QWeb/SCSS)

- [ ] ¿El asset está declarado en `__manifest__.py:assets`?
- [ ] ¿El componente se registra en `registry`?
- [ ] ¿La plantilla `t-name` coincide con el componente que la usa?

## Reporte sugerido

Incluir solo hallazgos verificados como mínimo:

- Ubicación (`archivo:línea`).
- Tipo de código muerto.
- Evidencia de ausencia de referencia.
- Riesgo de borrado.
- Acción recomendada.

Si hay dudas, marcar como `Sospechoso` y no proponer borrado inmediato.

## Pitfalls frecuentes en Odoo

1. Considerar muerto un método llamado solo desde XML.
2. Borrar archivos XML cargados por manifest pero no referenciados por import.
3. Ignorar dependencias cruzadas entre addons.
4. Eliminar assets registrados dinámicamente en frontend.
5. No verificar impacto en tests/tours.
