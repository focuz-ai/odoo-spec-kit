---
name: writing-skills
description: Use esta skill cuando necesite crear nuevas habilidades (skills) para agentes de IA, editar habilidades existentes o verificar su funcionamiento antes de integrarlas al kit.
author: Focuz AI
version: 1.0.0
---

# Skill: Creación y Edición de Habilidades (/writing-skills)

Esta skill establece la metodología de Desarrollo Guiado por Pruebas (TDD) adaptada a la creación y estructuración de documentación de procesos (skills) para agentes de IA.

---

## 1. Principio Core: TDD para Procesos

**Crear una skill es equivalente a aplicar TDD a la documentación.**
No se debe escribir una skill si no se ha observado primero a un agente fallar o cometer un error que justifique su existencia (fase **RED**). El documento de la skill representa el "código de producción" que resuelve el fallo (fase **GREEN**). Refinar los prompts y simplificar las instrucciones equivale a la fase de **REFACTOR**.

---

## 2. Estructura de un Archivo `SKILL.md`

Todo archivo de skill debe residir en su propia carpeta bajo `ai-specs/skills/[nombre-skill]/SKILL.md` y cumplir con la siguiente estructura:

### Frontmatter (YAML)
- Contiene los metadatos obligatorios `name` y `description`.
- **Regla Crítica de la Descripción**: Debe describir **CUÁNDO** usar la skill (condiciones de disparo y síntomas del problema) y **NUNCA** resumir el proceso o los pasos internos que realiza la skill.
  - *Mal*: `description: Use para validar código y corregir con un bucle de 3 intentos.` (El agente leerá la descripción resumida y omitirá leer el archivo de la skill completo).
  - *Bien*: `description: Use cuando la suite de pruebas reporte fallas de ejecución o errores de transacciones en la base de datos.`

```markdown
---
name: nombre-skill-con-guiones
description: Use cuando [síntomas, contextos y condiciones de disparo específicas]
---

# Nombre de la Skill

## Resumen
Explicación corta de la técnica o patrón en 1 o 2 líneas.

## Cuándo usar
- Síntomas y situaciones que disparan la skill.
- Cuándo **no** usar.

## Flujo de Trabajo / Patrón
Pasos detallados que el agente debe ejecutar.

## Errores Comunes
Antipatrones y cómo corregirlos.
```

---

## 3. Cuándo Crear una Skill

- **Sí**: Cuando la técnica o solución de Odoo no sea obvia, se repita constantemente a lo largo del proyecto, y requiera un criterio de decisión no automatizable mediante linters sencillos.
- **No**: Para guías de un solo uso, documentación redundante de APIs nativas de Odoo, o reglas de estilo sencillas que se validan mejor con Ruff o Pylint.
