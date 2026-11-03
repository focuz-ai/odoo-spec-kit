---
description: >
  Reglas base y lineamientos absolutos que gobiernan el comportamiento de todos los agentes. Es la única fuente de
  verdad global de Odoo.
---

```yaml
# Contexto Global del Proyecto
ODOO_TARGET_VERSION: "16.0"
EDITION: "Enterprise / Community"
```

# Reglas de Agentes y Estándares de Ingeniería

## 1. Principios Core

- **Tareas pequeñas, una a la vez**: Trabajar siempre en pasos pequeños (baby steps). Nunca avanzar más de un paso a la
  vez.
- **Spec-Driven Development (SDD)**: Comenzar definiendo las especificaciones detalladas del desarrollo antes de
  escribir código. Diseñar modelos, vistas, seguridad y flujos de negocio primero. Los tests unitarios y de integración
  se construyen y ejecutan como herramientas de verificación post-implementación.
- **Anti-Vibe-Coding**: Bajo ninguna circunstancia se debe saltar de la historia de usuario (User Story) directamente a
  escribir código. Las fases de propuesta (`proposal.md`), diseño (`design.md`) y lista de tareas (`tasks.md` /
  `task.md`) son obligatorias antes de proceder con el desarrollo físico de los cambios.
- **Seguridad de tipos**: Todo el código debe estar debidamente tipado (Type Hints en Python y JSDoc/OWL tipado en
  JavaScript).
- **Nombres claros**: Utilizar nombres claros y descriptivos para todas las variables, métodos y modelos (siguiendo las
  convenciones de Odoo).
- **Cambios incrementales**: Preferir cambios pequeños y enfocados sobre modificaciones grandes y complejas.
- **Cuestionar suposiciones**: Cuestionar siempre las suposiciones e inferencias sobre el modelo o las dependencias.

## 2. Estándares de Idioma

- **Español (Solo para Documentación y Artefactos OpenSpec)**:
  - Artefactos de diseño de OpenSpec (historias de usuario, especificaciones técnicas de diseño, planes de
    implementación, walkthroughs y `tasks.md`).
  - Documentación técnica orientada al repositorio (README del proyecto y guías de configuración externas).
- **Inglés (Para TODO el Desarrollo y Código Fuente, sin excepciones)**:
  - Código fuente Python (modelos, campos, métodos, decoradores, comentarios, mensajes de error técnicos y logs).
  - Código fuente JavaScript (componentes OWL, lógica de frontend, comentarios y JSDoc).
  - Vistas XML, reportes XML, data XML y archivos de seguridad CSV (nombres técnicos de grupos y reglas).
  - **Textos orientados al usuario en el código** (`string=`, `help=`, `_("...")` y el contenido de las plantillas
    QWeb): se escriben en inglés como idioma base. **Nunca** se codifican textos en español directamente en el código;
    la traducción a cualquier idioma se gestiona exclusivamente vía i18n (archivos `.po`), siendo `es_419` (español de
    Latinoamérica) la traducción predeterminada.
  - El archivo de manifiesto de Odoo (`__manifest__.py`), incluyendo el título, descripción, sumario y metadatos del
    addon.
  - Pruebas y tests (nombres de métodos de test, aserciones y descripciones de pruebas en Python y JS QUnit).
  - Mensajes de commit de Git y descripciones de Pull Requests (siguiendo el formato oficial de Odoo, ej:
    `[ADD] module_name: add invoice generation logic`).

## 3. Estándares Específicos

Para directrices y estándares específicos de diferentes áreas del proyecto, consulte:

- [Estándares Backend](./backend-standards.md) - Desarrollo de modelos ORM, controladores web, wizards, reportes,
  seguridad y pruebas backend en Odoo.
- [Estándares Frontend](./frontend-standards.md) - Componentes OWL 2, plantillas QWeb, SCSS, assets y pruebas unitarias
  con QUnit.
- [Directrices de Estilo de Código (Coding Guidelines)](./coding-guidelines.md) - Síntesis oficial de estilos de Odoo
  para Python, JS, CSS y XML.
- [Directrices de Git (Git Guidelines)](./git-guidelines.md) - Estructura oficial de commits de Odoo y flujos de
  integración.
- [Estándares de Documentación](./documentation-standards.md) - Estructura y mantenimiento de la documentación técnica y
  archivos de configuración de IA.
- [Topología Core de Odoo](./odoo-core-topology.md) - Reglas inquebrantables de modelos base y uso de MCP para
  introspección.
- [Integración y Controladores (RPC & Controllers)](./rpc-and-controllers.md) - XML-RPC/JSON-RPC y controladores
  HTTP/web personalizados.
- [Guía de Setup y Desarrollo](./development-guide.md) - Configuración del entorno, comandos `odoo-bin` y pipeline de
  calidad pre-commit.
- [Pasos Obligatorios OpenSpec](./openspec-tasks-mandatory-steps.md) - Lista de verificación y reglas obligatorias para
  tareas del workflow OpenSpec.

## 4. Skills del Proyecto

- Las skills del proyecto residen en `ai-specs/skills`.
- Cuando una solicitud coincida con una skill, cargue y siga el archivo `SKILL.md` correspondiente automáticamente antes
  de continuar.
- Cargue también cualquier archivo referenciado en la carpeta de la skill (por ejemplo, `references/*.md`).

## 5. Requisito de Modelo de Planificación

Los flujos de planificación y análisis deben ejecutarse con un modelo de razonamiento alto (como Claude 3 Opus o
similar).

Esto aplica a las tareas de:

- `enrich-us`
- `openspec-ff-change`
- `openspec-continue-change`

Antes de iniciar estas tareas, verifique que la sesión esté utilizando razonamiento alto. Si no es así, corríjalo
configurando el modelo apropiado en la herramienta del copilot.

## 6. Integridad de Symlinks y Portabilidad Multi-Agente

- **Origen Canónico**: Mantener los artefactos reutilizables en `ai-specs/` como el origen canónico. Las rutas
  específicas de agentes (como `.claude/`, `.cursor/`, `.agents/`) deben referenciarlos mediante symlinks.
- **Seguridad en Actualizaciones**: Cada vez que un archivo sea renombrado, movido o cambie de extensión, verifique y
  actualice todos los symlinks que apuntan a él antes de finalizar la tarea.
- **Enlace de Nuevos Artefactos**: Al crear una nueva skill o agente en `ai-specs/` que requiera exposición
  multi-agente, cree los symlinks correspondientes en las carpetas específicas de cada agente.
- **Puerta de Cierre**: Un cambio se considera incompleto si deja symlinks rotos o artefactos canónicos duplicados.

## 7. Actualizaciones de Artefactos OpenSpec

Cuando se reciba una solicitud de cambio tras la fase de aplicación (`/apply`) y antes del archivado (`/archive`), se
debe tratar como una actualización de la especificación técnica en primer lugar:

1. Actualizar los artefactos de diseño OpenSpec afectados (historias de usuario, especificaciones técnicas y
   `tasks.md`).
2. Implementar los cambios en el código únicamente después de que los artefactos de especificación reflejen la nueva
   solicitud.
3. Ejecutar de nuevo la validación del workflow (`/verify`, `/odoo-security-audit` y `/odoo-adversarial-review`) antes
   de archivar.

## 8. Comandos de Desarrollo y Calidad

> Estos comandos operan sobre el proyecto Odoo destino, no sobre este kit. Consulte `docs/development-guide.md` para el
> setup completo (venv, PostgreSQL, `odoo.conf`).

- **Tests backend (módulo):** `python odoo-bin -c odoo.conf -d <bd> --test-enable --stop-after-init -i <module>`
- **Tests filtrados por tag:** añadir `--test-tags /<module>:post_install`
- **Un solo test / clase:** `--test-tags /<module>:<TestClass>.<test_method>`
- **Tours frontend (Chrome headless):** `--test-tags /<module>:HttpCase`
- **Gate de calidad local (obligatorio antes de commit):** `python -m pre_commit run --all-files` → Ruff (`.ruff.toml`),
  Prettier (`prettier.config.cjs`, XML/JS/SCSS) y Pylint-Odoo (`.pylintrc`, `.pylintrc-mandatory`).

## 9. Orden Canónico del Workflow OpenSpec

- **Flujo core (orquestado, 4 pasos):** `/odoo-enrich-us` → `/propose` → `/odoo-build-and-qa` → `/odoo-ship`
- **Flujo extendido (granular, 8 pasos):** `/odoo-enrich-us` → `/propose` → `/apply` → `/verify` →
  `/odoo-security-audit` → `/odoo-adversarial-review` → `/archive` → `/odoo-commit`
- La revisión adversarial es Red Team puro: emite veredicto (PASS / PASS WITH GAPS / FAIL) sin reparar; la
  autoreparación la gestiona `/odoo-build-and-qa`.
- Las skills viven en `ai-specs/skills/` (origen canónico) y se exponen vía symlink a `.claude/`, `.cursor/` y
  `.agents/`.
