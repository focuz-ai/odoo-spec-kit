---
description: Este documento contiene todas las reglas y directrices de desarrollo para este proyecto, aplicables a todos los agentes de IA (Claude, Cursor, Codex, Gemini, etc.).
alwaysApply: true
---

## 1. Principios Core

- **Tareas pequeñas, una a la vez**: Trabajar siempre en pasos pequeños (baby steps). Nunca avanzar más de un paso a la vez.
- **Spec-Driven Development (SDD)**: Comenzar definiendo las especificaciones detalladas del desarrollo antes de escribir código. Diseñar modelos, vistas, seguridad y flujos de negocio primero. Los tests unitarios y de integración se construyen y ejecutan como herramientas de verificación post-implementación.
- **Seguridad de tipos**: Todo el código debe estar debidamente tipado (Type Hints en Python y JSDoc/OWL tipado en JavaScript).
- **Nombres claros**: Utilizar nombres claros y descriptivos para todas las variables, métodos y modelos (siguiendo las convenciones de Odoo).
- **Cambios incrementales**: Preferir cambios pequeños y enfocados sobre modificaciones grandes y complejas.
- **Cuestionar suposiciones**: Cuestionar siempre las suposiciones e inferencias sobre el modelo o las dependencias.

## 2. Estándares de Idioma

- **Español (Solo para Documentación y Artefactos OpenSpec)**:
    - Artefactos de diseño de OpenSpec (historias de usuario, especificaciones técnicas de diseño, planes de implementación, walkthroughs y `tasks.md`).
    - Documentación técnica orientada al repositorio (README del proyecto y guías de configuración externas).
- **Inglés (Para toda la Programación y Código Fuente)**:
    - Código fuente Python (modelos, campos, métodos, decoradores, comentarios, mensajes de error técnicos y logs).
    - Código fuente JavaScript (componentes OWL, lógica de frontend, comentarios y JSDoc).
    - Vistas XML, reportes XML, data XML y archivos de seguridad CSV (nombres técnicos de grupos y reglas).
    - El archivo de manifiesto de Odoo (`__manifest__.py`), incluyendo el título, descripción, sumario y metadatos del addon.
    - Pruebas y tests (nombres de métodos de test, aserciones y descripciones de pruebas en Python y JS Hoot).
    - Mensajes de commit de Git y descripciones de Pull Requests (siguiendo el formato oficial de Odoo, ej: `[ADD] module_name: add invoice generation logic`).

## 3. Estándares Específicos

Para directrices y estándares específicos de diferentes áreas del proyecto, consulte:

- [Estándares Backend](./backend-standards.md) - Desarrollo de modelos ORM, controladores web, wizards, reportes, seguridad y pruebas backend en Odoo.
- [Estándares Frontend](./frontend-standards.md) - Componentes OWL 2, plantillas QWeb, SCSS, assets y pruebas unitarias con HOOT.
- [Directrices de Estilo de Código (Coding Guidelines)](./coding-guidelines.md) - Síntesis oficial de estilos de Odoo para Python, JS, CSS y XML.
- [Directrices de Git (Git Guidelines)](./git-guidelines.md) - Estructura oficial de commits de Odoo y flujos de integración.
- [Estándares de Documentación](./documentation-standards.md) - Estructura y mantenimiento de la documentación técnica y archivos de configuración de IA.
- [Pasos Obligatorios OpenSpec](./openspec-tasks-mandatory-steps.md) - Lista de verificación y reglas obligatorias para tareas del workflow OpenSpec.

## 4. Skills del Proyecto

- Las skills del proyecto residen en `ai-specs/skills`.
- Cuando una solicitud coincida con una skill, cargue y siga el archivo `SKILL.md` correspondiente automáticamente antes de continuar.
- Cargue también cualquier archivo referenciado en la carpeta de la skill (por ejemplo, `references/*.md`).

## 5. Requisito de Modelo de Planificación

Los flujos de planificación y análisis deben ejecutarse con un modelo de razonamiento alto (como Claude 3 Opus o similar).

Esto aplica a las tareas de:
- `enrich-us`
- `openspec-ff-change`
- `openspec-continue-change`

Antes de iniciar estas tareas, verifique que la sesión esté utilizando razonamiento alto. Si no es así, corríjalo configurando el modelo apropiado en la herramienta del copilot.

## 6. Integridad de Symlinks y Portabilidad Multi-Agente

- **Origen Canónico**: Mantener los artefactos reutilizables en `ai-specs/` como el origen canónico. Las rutas específicas de agentes (como `.claude/`, `.cursor/`, `.agents/`) deben referenciarlos mediante symlinks.
- **Seguridad en Actualizaciones**: Cada vez que un archivo sea renombrado, movido o cambie de extensión, verifique y actualice todos los symlinks que apuntan a él antes de finalizar la tarea.
- **Enlace de Nuevos Artefactos**: Al crear una nueva skill o agente en `ai-specs/` que requiera exposición multi-agente, cree los symlinks correspondientes en las carpetas específicas de cada agente.
- **Puerta de Cierre**: Un cambio se considera incompleto si deja symlinks rotos o artefactos canónicos duplicados.

## 7. Actualizaciones de Artefactos OpenSpec

Cuando se reciba una solicitud de cambio tras la fase de aplicación (`/apply`) y antes del archivado (`/archive`), se debe tratar como una actualización de la especificación técnica en primer lugar:

1. Actualizar los artefactos de diseño OpenSpec afectados (historias de usuario, especificaciones técnicas y `tasks.md`).
2. Implementar los cambios en el código únicamente después de que los artefactos de especificación reflejen la nueva solicitud.
3. Ejecutar de nuevo la validación del workflow (`/verify` y `/code-review`) antes de archivar.
