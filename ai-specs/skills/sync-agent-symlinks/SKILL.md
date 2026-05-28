---
name: sync-agent-symlinks
description:
  Sincroniza y mantiene la integridad de los enlaces simbólicos (symlinks) de skills y agentes desde ai-specs/ hacia
  .claude/, .cursor/ y .agents/.
author: Focuz.io
version: 1.0.0
---

# Skill: Sincronización de Enlaces Simbólicos (/sync-agent-symlinks)

Esta skill permite mantener alineados los directorios de copilots específicos (`.claude/`, `.cursor/`, `.agents/`) con
la fuente canónica de agentes y skills del proyecto: `ai-specs/`.

---

## Directrices y Reglas de Seguridad

- **Fuentes Canónicas**:
  - `ai-specs/skills/` (Directorio de skills).
  - `ai-specs/agents/` (Directorio de agentes).
- **Directorios Destino (Espejos)**:
  - `.claude/skills/` y `.claude/agents/`
  - `.cursor/skills/` y `.cursor/agents/`
  - `.agents/skills/` y `.agents/agents/` (Compatibilidad con Antigravity 2.0 / CLI).
- **Solo Symlinks**: Solo se deben gestionar entradas que correspondan a enlaces simbólicos que apunten a `ai-specs/`.
  Nunca elimine directorios reales o archivos locales creados por el usuario en las carpetas espejo.

---

## Flujo de Trabajo

### Paso 1: Inventario de Recursos

1. Leer los recursos físicos en la fuente canónica (`ai-specs/skills` y `ai-specs/agents`).
2. Listar el contenido de los directorios destino para identificar:
   - **Enlazados**: Symlinks válidos que apuntan al archivo canónico.
   - **Rotos**: Enlaces simbólicos cuyo destino físico ya no existe.
   - **Huérfanos**: Enlaces simbólicos de la política canónica que apuntan a un elemento eliminado.
   - **Conflictos**: Directorios o archivos reales (no enlaces) con el mismo nombre de un elemento canónico.

### Paso 2: Plan de Sincronización

Calcular las acciones requeridas para cada destino:

- `to_add`: Elementos canónicos nuevos ausentes en el destino.
- `to_fix`: Enlaces rotos que deben recrearse.
- `to_remove`: Enlaces huérfanos que deben eliminarse.
- `to_skip`: Conflictos y elementos externos que no deben tocarse.

### Paso 3: Aplicación Segura de Cambios

Ejecutar las operaciones utilizando comandos de terminal según el sistema operativo (en Windows, mediante PowerShell
`New-Item -ItemType SymbolLink` o `cmd /c mklink`):

```powershell
# Ejemplo de creación de enlace simbólico de skill en Windows (PowerShell)
New-Item -ItemType SymbolicLink -Path ".claude\skills\mi-skill" -Value "..\..\ai-specs\skills\mi-skill"
```

### Paso 4: Reporte final

Retornar un resumen de la sincronización en el chat indicando:

- Número de elementos canónicos sincronizados.
- Detalle por destino (agregados, corregidos, eliminados, conflictos).
