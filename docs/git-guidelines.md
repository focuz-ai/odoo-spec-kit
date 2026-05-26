# Directrices de Git y Commits de Odoo (Git Guidelines)

> [!IMPORTANT]
> Este documento sintetiza las directrices oficiales de Git y Commits de Odoo. Es mandatorio que todos los commits realizados en este repositorio sigan esta estructura y reglas de etiquetado para mantener un historial limpio, coherente y fácilmente auditable.

---

## 1. Estructura del Mensaje de Commit

Cada mensaje de commit debe estar estructurado en dos partes: un título corto (cabecera) y una descripción larga (cuerpo), separados por una línea en blanco.

```text
[TAG] modulo_tecnico: breve descripcion en presente y menor de 50 caracteres

Explicación detallada del POR QUÉ se realiza este cambio (cuerpo del commit).
Aquí se detalla el problema de negocio o el fallo técnico y cómo esta solución
lo aborda. 

Referencias a tareas o incidencias:
task-12345
Fixes #456
```

---

## 2. Etiquetas Oficiales (Tags)

El título debe iniciar estrictamente con una etiqueta en mayúsculas que indique la naturaleza del cambio:

| Tag | Significado / Cuándo Usarlo |
|---|---|
| **`[ADD]`** | Añadir nuevos archivos, nuevos modelos, vistas, datos o lógica de negocio. |
| **`[FIX]`** | Corregir un fallo, bug de ejecución, error XML o comportamiento incorrecto. |
| **`[IMP]`** | Mejorar o refinar código existente, interfaces de usuario o flujos de negocio sin cambiar el comportamiento principal. |
| **`[REF]`** | Refactorizar código para mejorar su diseño interno, sin alterar su funcionalidad externa. |
| **`[REM]`** | Eliminar archivos, campos, vistas o código obsoleto. |
| **`[REV]`** | Revertir un commit anterior que causó problemas. |
| **`[MOV]`** | Mover archivos, código o directorios de ubicación. |
| **`[REL]`** | Relativo a lanzamientos de versiones o releases. |
| **`[CLN]`** | Limpieza de código (formatting, comentarios, eliminaciones menores) sin cambios de lógica. |
| **`[LINT]`** | Correcciones de estilo indicadas por Ruff, Pylint u otras herramientas estáticas de análisis. |
| **`[PERF]`** | Mejoras orientadas exclusivamente a la velocidad o consumo de recursos (prefetch, queries sql). |
| **`[I18N]`** | Cambios relativos exclusivamente a archivos de traducción (`.pot`, `.po`). |
| **`[MERGE]`** | Commits específicos de combinación de ramas. |
| **`[CLA]`** | Firmas de acuerdos de licencia o copyright. |

---

## 3. Reglas para la Cabecera del Commit

- **Nombre del módulo**: Utilizar el nombre técnico del directorio del módulo en minúsculas (ej. `account`, `sale`, `mi_modulo_contable`). Si el cambio afecta a varios módulos o infraestructura, usar `models`, `views` o `core` según corresponda.
- **Formato del título**: Redactar en tiempo presente imperativo. Debe responder a la frase: *"Si se aplica, este commit `<título>`"* (ej. `[FIX] account: corregir calculo de impuestos` en lugar de `[FIX] account: calculo corregido`).
- **Longitud**: Mantener el título por debajo de los 50 caracteres para evitar recortes en la interfaz de Git.

---

## 4. Cuerpo del Commit (Descripción Larga)

- **Explicar el POR QUÉ, no el QUÉ**: El código en sí (el diff) ya muestra *qué* cambió. La descripción larga debe enfocarse en explicar el problema original, la justificación del cambio, el por qué se eligió esa solución y las implicaciones colaterales.
- **Referencias obligatorias**: Si el cambio corresponde a una historia de usuario, ticket de soporte o reporte de fallo, incluya las referencias de forma explícita al final del cuerpo:
    - Para tareas de Plane o Jira: `task-123456`
    - Para incidencias de GitHub: `Fixes #456` o `Closes #456`
    - Para tickets de Odoo Enterprise (OPW): `opw-789012`

---

## 5. Ejemplos de Mensajes de Commit Correctos

### Ejemplo 1: Corrección de un fallo (Bugfix)
```text
[FIX] account_asset: corregir la fecha de prorata en el cálculo lineal

Cuando un activo lineal de modelo importado no tiene fecha de adquisición inicial
declarada, la fecha de prorata alucinaba al primer día del año actual en lugar de
tomar la fecha del inicio del periodo contable configurado.

Se añade una validación de fallback al método `_compute_prorata_date` para resolver
este comportamiento y se agrega el caso de prueba correspondiente.

task-987654
```

### Ejemplo 2: Añadir funcionalidad (Feature)
```text
[ADD] contabilidad_local: integrar modelo de conciliación personalizada

Se añade un nuevo modelo de negocio `contabilidad.conciliacion.regla` para automatizar
el mapeo de impuestos y cuentas según el concepto del extracto bancario.

Incluye:
- Vistas form y list declarativas.
- Reglas de seguridad básica y ACLs.
- Prueba unitaria en `TransactionCase` para verificar el matching automático.

task-123456
```
