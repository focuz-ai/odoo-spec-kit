---
name: commit-odoo
description:
  Crea commits y abre Pull Requests estructurados siguiendo las directrices oficiales de
  Odoo (Git Guidelines) y en idioma español.
author: Focuz AI
version: 1.0.0
---

# Skill: Crear Commit y PR Estilo Odoo (/commit-odoo)

Esta skill guía al agente en el empaquetado de sus cambios en un commit Git y la
posterior creación o actualización de un Pull Request en GitHub, adhiriéndose al
estándar oficial de contribuciones de Odoo 17.0.

---

## Instrucciones de Ejecución

Procese y empaquete los cambios locales. Siga estos pasos:

### 1. Evaluar Modo Dry-Run (Solo-Texto)

Si el usuario solicita explícitamente "dry run", "solo mensaje", "no tocar git" o
similar:

- Determine los archivos modificados.
- Redacte el mensaje de commit propuesto en una caja de código y muéstrelo al usuario.
- **No ejecute** comandos como `git add`, `git commit` o `git push`. Termine aquí.

### 2. Inspeccionar Cambios y Rama

- Ejecute `git status` y `git diff` para identificar qué archivos han sido modificados.
- Asegúrese de que se encuentra en la rama de característica correspondiente
  (`feature/[nombre-cambio]`).

### 3. Redactar el Mensaje de Commit (Estándar Odoo)

El mensaje de commit debe cumplir con las directrices oficiales definidas en
`docs/git-guidelines.md`:

- **Idioma**: El contenido explicativo debe ser redactado en **Español**.
- **Línea de Asunto**: Debe seguir la estructura:
  `[TAG] nombre_modulo: descripción corta del cambio (< 50 caracteres)`
  - _Ejemplo_: `[FIX] account_invoice_local: corregir redondeo de impuestos`
  - _Tags permitidos_: `[ADD]`, `[FIX]`, `[IMP]`, `[REF]`, `[REM]`, `[CLN]`, `[PERF]`,
    etc.
  - _Nombre del módulo_: Nombre técnico del directorio del addon (ej. `account`).
- **Descripción Larga (Cuerpo)**:
  - Deje una línea en blanco tras el asunto.
  - Explique el **POR QUÉ (WHY)** se hizo el cambio, no el _qué_ (el qué ya está visible
    en el código).
  - Incluya la referencia a la tarea o ID: `task-123` o `Fixes #123`.

### 4. Realizar Commit y Push

- Agregue los archivos al stage de git.
- Ejecute el commit con el mensaje estructurado en el paso anterior.
- Suba la rama al repositorio remoto (`git push origin <rama>`).

### 5. Crear Pull Request (GitHub CLI)

Si el CLI de GitHub (`gh`) está configurado y disponible:

- Ejecute `gh pr create` para abrir un Pull Request de la rama activa hacia la rama
  base.
- **Título del PR**: Alineado al commit (ej.
  `[ADD] mi_modulo: agregar facturación local`).
- **Descripción**: Resumen del objetivo, enlaces a tickets de Jira/Plane y confirmación
  de que las pruebas de `/verify` y `/code-review` pasaron exitosamente.

### 6. Reporte Final

Muestre al usuario un resumen detallado que incluya:

- Archivos incluidos en el commit.
- El mensaje de commit utilizado.
- El enlace (URL) del PR creado.
