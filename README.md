# Odoo Spec Kit: Desarrollo de Odoo Asistido por IA y OpenSpec

**odoo-spec-kit** es un kit de configuración y estándares técnicos portable diseñado para optimizar el desarrollo de módulos en **Odoo** (Community y Enterprise) mediante asistentes de Inteligencia Artificial (copilots como Claude, Cursor, Gemini/Antigravity y Copilot).

Este repositorio contiene un conjunto exhaustivo de reglas de desarrollo, directrices de estilo y configuraciones de agentes de IA diseñadas para trabajar sin fisuras con múltiples herramientas de desarrollo asistido. La configuración es portable y puede importarse a cualquier proyecto Odoo para proporcionar una asistencia coherente y de alta calidad.

Se recomienda encarecidamente utilizar este kit en combinación con frameworks de desarrollo guiado por especificaciones como [OpenSpec](https://github.com/Fission-AI/OpenSpec).

---

## 📋 Tabla de Contenidos
1. [Estructura del Repositorio](#-estructura-del-repositorio)
2. [Soporte Multi-Copiloto](#-soporte-multi-copiloto)
3. [Inicio Rápido](#-inicio-rápido)
4. [Verificación de la Configuración (Obligatorio)](#-verificación-de-la-configuración-obligatorio)
5. [Uso: Workflow Oficial de OpenSpec](#-uso-workflow-oficial-de-openspec)
6. [Reglas Core de Desarrollo](#-reglas-core-de-desarrollo)
7. [Beneficios del Kit](#-beneficios-del-kit)
8. [Personalización](#-personalización)
9. [Contexto Técnico de Referencia](#-contexto-técnico-de-referencia)
10. [Contribuciones](#-contribuciones)
11. [Agradecimientos y Créditos](#-agradecimientos-y-créditos)
12. [Licencia](#-licencia)

---

## 📁 Estructura del Repositorio

```text
.
├── docs/                             # Contexto técnico y estándares de ingeniería
│   ├── base-standards.md             # Reglas maestras (SDD, español, workflow)
│   ├── backend-standards.md          # Estándares ORM, Seguridad, SQL y XML views
│   ├── frontend-standards.md         # Componentes OWL 2, SCSS y QUnit testing
│   ├── coding-guidelines.md          # Directrices oficiales de código de Odoo
│   ├── git-guidelines.md             # Reglas y tags oficiales de commits de Odoo
│   ├── development-guide.md          # Guía de instalación y comandos odoo-bin
│   ├── data-model.md                 # Modelo de datos contable de ejemplo
│   ├── openspec-tasks-mandatory-steps.md # Pasos obligatorios del framework
│   └── api-spec.md                   # Especificación de endpoints y controladores
│
├── ai-specs/
│   ├── agents/                       # Definiciones de roles de agentes de IA
│   │   ├── odoo-module-developer.md  # Agente backend (Modelos, XML, Seguridad)
│   │   ├── odoo-owl-developer.md     # Agente frontend (OWL 2, QWeb, QUnit)
│   │   └── product-strategy-analyst.md # Analista funcional de producto Odoo
│   │
│   └── skills/                       # Habilidades y flujos reutilizables (skills)
│
├── config/                           # Archivos de configuración local
│   └── local.paths.example.json      # Plantilla de rutas locales (Odoo Community/Enterprise)
│
├── scripts/                          # Scripts utilitarios
│   └── setup_assistant.py            # Asistente de configuración e inicialización de rutas
│
├── config/                           # Archivos de configuración local
│   └── local.paths.example.json      # Plantilla de rutas locales (Odoo Community/Enterprise)
│
├── scripts/                          # Scripts utilitarios
│   └── setup_assistant.py            # Asistente de configuración e inicialización de rutas
│
├── AGENTS.md, CLAUDE.md, GEMINI.md   # Accesos de copilots apuntando a base-standards
├── .pre-commit-config.yaml           # Configuración de hooks pre-commit para calidad de código
├── .ruff.toml                        # Configuración de linter Ruff para Python/Odoo
└── .pylintrc                         # Configuración de linter Pylint (pylint-odoo)
```

---

## 🤖 Soporte Multi-Copiloto

Este repositorio utiliza **enlaces simbólicos (symlinks)** y **convenciones de nombres** para dar soporte a múltiples copilots de IA de forma nativa sin duplicar archivos en el espacio de trabajo:

- **`AGENTS.md`** → Reglas genéricas de agentes (compatible con la mayoría de copilots).
- **`CLAUDE.md`** → Optimizado para Claude/Cursor.
- **`GEMINI.md`** → Optimizado para Google Gemini.
- **`codex.md`** → Optimizado para GitHub Copilot/Codex.

Todos estos archivos enlazan a la misma fuente de verdad en `docs/base-standards.md`, asegurando la coherencia entre diferentes herramientas de IA y permitiendo personalizaciones para copilots específicos.

### ¿Por qué este Enfoque?

- ✅ **Única Fuente de Verdad**: Reglas core mantenidas en un solo lugar (`base-standards.md`).
- ✅ **Compatibilidad de Copilots**: Cada herramienta de IA encuentra su configuración usando su nombre preferido.
- ✅ **Cero Configuración Manual**: Se importa en un nuevo proyecto Odoo y funciona de inmediato.
- ✅ **Fácil de Actualizar**: Al actualizar las reglas una vez, todos los copilots se benefician de inmediato.
- ✅ **Portable**: Estructura fácilmente copiable a cualquier proyecto.

---

## 🚀 Inicio Rápido

Siga estos pasos para integrar el kit en su flujo de trabajo de desarrollo:

### 1) Instalar e Inicializar OpenSpec

OpenSpec es la herramienta recomendada para guiar el flujo de desarrollo de la IA a través de especificaciones. Requiere **Node.js v20.19.0 o superior** instalado en el sistema.

Instale OpenSpec globalmente desde su terminal:
```bash
npm install -g @fission-ai/openspec@latest
```

Luego, diríjase a la carpeta de su proyecto Odoo e inicialice la estructura de OpenSpec:
```bash
cd su-proyecto-odoo
openspec init
```

Si quieres el flujo de trabajo expandido (`/opsx:new`, `/opsx:continue`, `/opsx:ff`, `/opsx:verify`, `/opsx:bulk-archive`, `/opsx:onboard`), selecciónalo con `openspec config profile` y aplícalo con `openspec update`.

### 2) Importar el Kit en tu Proyecto

Copie todo el contenido de este repositorio en la raíz de su proyecto Odoo. Al importar, asegúrese de no sobreescribir archivos específicos del proyecto que ya existan (como el `README.md` original de su módulo):

```bash
# Clone or copy this repository into your project (`-n`: do not overwrite existing files so you keep project's original README)
cp -rn odoo-spec-kit/* your-project/
```

Usar skill `ai-specs\skills\sync-agent-symlinks` en el Copilito de su elección para mantener alineados los symlinks de `.agents`, `.claude` y `.cursor`.

### 3) Personalizar `docs/` para tu Proyecto (Obligatorio)

Este paso es obligatorio. Si lo omite, su asistente de IA utilizará contexto técnico genérico en lugar del contexto de su proyecto real.

Actualice los archivos en `docs/` para que coincidan con su base de datos de desarrollo, módulos personalizados, dependencias de Odoo, flujos contables y localizaciones requeridas. Consulte la sección [Personalización](#-personalización) para obtener instrucciones detalladas.

### 4) Apuntar la Configuración de OpenSpec a `docs/` y `ai-specs/`

Después de inicializar OpenSpec e importar el kit, debe indicarle a OpenSpec cómo cargar y usar las reglas y agentes del proyecto. Envíe el siguiente prompt a su copilot para configurar de forma automática el archivo `config.yml`:

```text
Actualiza el contexto de mi config.yml de openspec para referenciar la estructura de docs y ai-specs de este repositorio.

Requisitos:
- Usar docs/base-standards.md como única fuente de verdad.
- Incluir docs/backend-standards.md, docs/frontend-standards.md, docs/documentation-standards.md.
- Incluir docs/api-spec.yml y docs/data-model.md.
- Indicarle al agente que adopte ai-specs/agents/odoo-module-developer.md para tareas de backend y vistas XML, y ai-specs/agents/odoo-owl-developer.md para tareas de frontend OWL 2/SCSS.
- Mencionar ai-specs/skills como guía de flujo de trabajo.
- Mantener todas las rutas relativas a la raíz del proyecto.

```

Ejemplo (`config.yml`):

```yml
context: |
  Tech stack: TypeScript, Node.js, Express, Prisma, Domain-Driven Design (DDD)
  Architecture: Clean Architecture with Domain, Application, and Presentation layers
  We use conventional commits
  Domain: LTI (Leadership. Technology. Impact) ATS platform
  All code, comments, documentation, and technical artifacts must be in English

  Project specs (single source of truth): All artifact creation and implementation MUST follow the project's technical context in ai-specs/. Read and apply these when creating or implementing:
  - docs/base-standards.md — core principles, TDD, language standards, links to backend/frontend/docs standards
  - docs/backend-standards.md — API, database, testing, security (backend changes)
  - docs/frontend-standards.md — React, UI/UX (frontend changes)
  - docs/api-spec.yml — API contracts and endpoint definitions
  - docs/data-model.md — domain and data model
  - docs/documentation-standards.md — docs structure and maintenance
  For implementation: adopt the relevant agent from ai-specs/agents/ (e.g. backend-developer.md for backend, frontend-developer.md for frontend). Use ai-specs/skills/ for workflow guidance when applicable.

# Per-artifact rules (optional)
# Add custom rules for specific artifacts.
rules:
  # Global: apply ai-specs when creating any artifact
  _global:
    - Before creating any artifact, read and apply docs/base-standards.md
    - For backend-related artifacts, read docs/backend-standards.md and adopt guidelines from ai-specs/agents/backend-developer.md
    - For frontend-related artifacts, read docs/frontend-standards.md and adopt guidelines from ai-specs/agents/frontend-developer.md
    - Use docs/api-spec.yml and docs/data-model.md for API and data consistency in specs and tasks
```

---

## ✅ Verificación de la Configuración (Obligatorio)

Realice este paso de validación después de completar los pasos de configuración y setup descritos anteriormente. Su copilot o agente de IA debería cargar automáticamente el archivo de configuración base al iniciar su sesión:

- **Claude/Cursor**: Carga `CLAUDE.md` → Enlazado a `docs/base-standards.md`.
- **GitHub Copilot**: Carga `codex.md` → Enlazado a `docs/base-standards.md`.
- **Gemini**: Carga `GEMINI.md` → Enlazado a `docs/base-standards.md`.

Todas las rutas de directrices técnicas y las habilidades específicas de los agentes están mapeadas para funcionar correctamente y ser auto-cargadas sin necesidad de realizar ajustes manuales en los editores.

---

## 💡 Uso: Workflow Oficial de OpenSpec

El desarrollo utilizando **odoo-spec-kit** sigue un ciclo de vida estrictamente verificado:

1. **`/odoo-enrich-us`**: Analiza y enriquece el requerimiento de negocio conectándose a Jira o Plane MCP, y buscando de forma obligatoria en el código real de Odoo en lugar de adivinar nombres de campos.
2. **`/propose`**: Diseña la especificación técnica en markdown detallando modelos, campos, lógica de negocio y pruebas.
3. **`/apply`**: Escribe el código fuente de forma incremental.
4. **`/verify` + `/odoo-security-audit` + `/odoo-adversarial-review`**:
   - Tras completar el código, el agente prueba la especificación con `/verify`.
   - Luego, se ejecutan las auditorías de seguridad y funcionales que activan el **Bucle de Autoreparación** si hay fallos en las pruebas.
5. **`/archive`**: Archiva el ciclo de cambios.
6. **`/odoo-commit`**: Crea commits enfocados y gestiona PR después de la verificación con el formato oficial de Odoo (ej. `[ADD] mi_modulo: agregar facturación local`).

### Opcional: Integraciones MCP (Jira + Plane)

Este flujo de trabajo se ve reforzado con servidores de Protocolo de Contexto de Modelo (MCP) integrados en el flujo. Estos son opcionales y pueden omitirse o reemplazarse por herramientas equivalentes:

- **Jira MCP / Plane MCP (recomendados en `/odoo-enrich-us`)**: Permiten al agente leer directamente los tickets desde sus tableros de gestión para enriquecer las historias de usuario sin necesidad de copiar y pegar manualmente.

### Ejemplo: Flujo de Extremo a Extremo (End-to-End)

Primer paso opcional (recomendado para ambos flujos): crea un worktree dedicado antes de ejecutar el flujo de comandos y límpialo al terminar. El skill `using-git-worktrees` puede automatizar esto.

#### 1. Flujo Core (Orquestado - 4 Pasos)
Este es el flujo principal recomendado. Agrupa la construcción, auditoría, auto-reparación y cierre en orquestadores autónomos:

```bash
/odoo-enrich-us TICKET-101
/propose TICKET-101
/odoo-build-and-qa TICKET-101
/odoo-ship TICKET-101
```

#### 2. Flujo Extendido (Paso a Paso - 8 Pasos)
Útil si necesitas control granular o depuración manual en cada fase de la implementación y auditoría:

```bash
/odoo-enrich-us TICKET-101
/propose TICKET-101
/apply TICKET-101
/verify TICKET-101
/odoo-security-audit TICKET-101
/odoo-adversarial-review TICKET-101
/archive TICKET-101
/odoo-commit
```

Los artefactos se gestionan y guardan a través de las carpetas de OpenSpec durante este flujo, incluyendo los reportes de pruebas unitarias y de revisión adversarial de seguridad.

### Habilidades (Skills) Útiles

Las habilidades del kit residen en `ai-specs/skills/` y se vinculan a `.agents/skills/`, `.claude/skills/` y `.cursor/skills/` para facilitar su descubrimiento:

- **`odoo-build-and-qa`** — Construye el código, verifica, realiza auditoría de seguridad y auto-repara en un bucle autónomo.
- **`odoo-code-auditing`** — Metodología estructurada en español para realizar auditorías de calidad de código y detectar deuda técnica en módulos Odoo.
- **`odoo-adversarial-review`** — Revisa la funcionalidad, rendimiento y cumplimiento de directrices del código Odoo. Incluye verificación contra el Spec Funcional (SDD) y un bucle de autoreparación autónomo ante fallos.
- **`odoo-commit`** — Crea commits y abre Pull Requests estructurados siguiendo las directrices oficiales de Odoo (Git Guidelines) y en idioma español.
- **`odoo-enrich-us`** — Analiza y enriquece historias de usuario con detalles técnicos completos y listos para implementación en Odoo EE siguiendo el Spec-Driven Development.
- **`odoo-explain`** — Enseña conceptos fundamentales y avanzados de Odoo (ORM, OWL, Contabilidad, Seguridad) cerrando brechas conceptuales mediante modelos mentales y cuestionarios interactivos.
- **`meta-prompt`** — Reescribe prompts utilizando las mejores prácticas de ingeniería de prompts para obtener resultados precisos y completos.
- **`odoo-scaffold`** — Inicializa la estructura de carpetas y archivos base de un nuevo módulo o addon para Odoo.
- **`odoo-test-runner`** — Ejecuta la suite de pruebas unitarias o de integración en Odoo, filtrando por módulo o etiqueta y extrayendo resultados detallados.
- **`odoo-security-audit`** — Realiza la auditoría estática de seguridad y permisos en módulos de Odoo EE. Cruza ACLs, reglas de registro, detecta inyecciones SQL y previene XSS en vistas QWeb.
- **`odoo-ship`** — Orquestador final que archiva el ticket completado y realiza el commit estructurado siguiendo los estándares de Odoo.
- **`show-spec-working`** — Úselo cuando se solicite una demostración ("show me X", "demo X") o revisión interactiva de una especificación, característica o ticket.
- **`sync-agent-symlinks`** — Analiza y sincroniza las habilidades de los agentes tras cambios en `ai-specs`. Mantiene alineados los symlinks de `.agents`, `.claude` y `.cursor`.
- **`update-docs`** — Identifica y actualiza la documentación técnica requerida basándose en los cambios implementados.
- **`using-git-worktrees`** — Aísla el trabajo en una característica creando o utilizando git worktrees antes de ejecutar planes de implementación.
- **`writing-skills`** — Crea nuevas skills, edita las existentes o verifica el funcionamiento de las skills antes de su despliegue.

---

## 📖 Reglas Core de Desarrollo

Todo el desarrollo del proyecto sigue los principios fundamentales definidos en `docs/base-standards.md`:

### Principios Clave

1. **Tareas pequeñas, una a la vez**: Avance siempre en baby steps. Nunca intente saltarse pasos de la especificación.
2. **Desarrollo Basado en Especificaciones (SDD)**: Defina las especificaciones detalladas antes de escribir código. Los tests son herramientas de verificación post-implementación.
3. **Seguridad de Tipos**: Todo el código de Python y JavaScript debe estar tipado (Type Hints y JSDoc).
4. **Nombres Claros**: Nombres descriptivos para variables, modelos y métodos del negocio siguiendo la convención de Odoo.
5. **Estricto Español**: Todos los comentarios, variables, documentación y artefactos deben estar en español.
6. **Manejo Seguro de Transacciones**: Prohibido usar `cr.commit()` manual. Odoo maneja las transacciones de forma segura.

### Estándares Específicos

- **Estándares Backend**: [docs/backend-standards.md](docs/backend-standards.md) (ORM, herencias, seguridad estática, SQL y XML views).
- **Estándares Frontend**: [docs/frontend-standards.md](docs/frontend-standards.md) (Componentes OWL 2, SCSS y QUnit testing).
- **Estándares de Documentación**: [docs/documentation-standards.md](docs/documentation-standards.md) (Reglas de idioma, triggers de actualización y auto-mejora).

---

## 🎯 Beneficios del Kit

### Para Desarrolladores

- ✅ **Consistencia del Código**: La IA genera vistas XPath estables y consultas seguras sin desviación de estilo.
- ✅ **Menos Bloqueos**: El bucle de autoreparación resuelve de forma autónoma tracebacks de compilación o fallos sencillos de aserciones de pruebas.
- ✅ **Mentoría Integrada**: Explicación conceptual interactiva al instante para nivelar conocimientos sobre Odoo.

### Para Equipos

- ✅ **Flexibilidad**: Los miembros del equipo pueden usar su copilot preferido manteniendo los mismos estándares.
- ✅ **Preservación del Conocimiento**: Los estándares de arquitectura y negocio están documentados en el kit, no solo en la cabeza de las personas.
- ✅ **Revisiones de Código Rápidas**: El código sigue patrones establecidos, agilizando el proceso de aprobación y mezcla (merge).

### Para Proyectos

- ✅ **Mantenibilidad a Largo Plazo**: Estructuración extensible (Think Extendable) forzada desde el primer día.
- ✅ **Documentación Viva**: Modelos de datos contables y especificaciones de APIs siempre sincronizados con los cambios de código.
- ✅ **Menor Deuda Técnica**: Buenas prácticas del ORM y prevención de inyección SQL con `odoo.tools.SQL` aplicados por defecto.

---

## 🔧 Personalización

### Adaptando el Kit a tu Proyecto

1. **Actualizar el contexto técnico**: Modifique los archivos en `docs/` para que coincidan con la pila de Odoo, la base de datos de desarrollo y las reglas del negocio de su proyecto.
2. **Ajustar los agentes**: Adapte las definiciones en `ai-specs/agents` para que coincidan con los roles de su equipo.
3. **Mapear recursos**: Utilice MCPs para enlazar los tableros de tareas o servidores de pruebas de la organización.
4. **Mantener la estructura de enlaces**: Recree las junctions y hardlinks correspondientes si añade nuevos agentes o habilidades.

### Ejemplo de Prompt: Adaptar el Contexto Técnico

Utilice este prompt con su copilot para adaptar el kit a su proyecto manteniendo la misma estructura base:

```text
Siguiendo la misma estructura base ya presente en docs/, actualiza todos los documentos de contexto técnico según los detalles específicos de este proyecto.

Requisitos:
- Mantener el mismo conjunto de documentos y nombres de archivo en docs/.
- Reemplazar el contenido genérico con el stack real del proyecto, sus patrones de arquitectura, convenciones de código y terminología de dominio.
- Actualizar los estándares de backend, frontend y documentación para reflejar las prácticas reales del equipo.
- Actualizar docs/api-spec.yml y docs/data-model.md para que coincidan con los endpoints y entidades reales del proyecto.
- Asegurar que todas las referencias sean internamente consistentes y estén alineadas entre sí dentro de docs/.
- Mantener todo en español y hacer que las guías estén listas para ser implementadas por agentes de IA.
```

### Mantenimiento de los Estándares

- **Fuente Única de Verdad**: Actualice siempre `base-standards.md` antes de realizar cambios de reglas secundarias.
- **Revisión del Equipo**: Las modificaciones a las reglas de desarrollo deben ser aprobadas mediante Pull Requests.
- **Integridad de Enlaces**: Tras renombrar o mover archivos, verifique y actualice todos los accesos en `.claude`, `.cursor` y `.agents`.

---

## 📚 Contexto Técnico de Referencia

### Ejemplos de Referencia (Contabilidad Odoo)

Los siguientes archivos están incluidos en este kit como ejemplos de referencia basados en el dominio de Contabilidad de Odoo:

- **Especificación de API/Controllers**: [docs/api-spec.md](docs/api-spec.md) (Endpoints JSON-RPC/REST).
- **Modelos de Datos**: [docs/data-model.md](docs/data-model.md) (Estructura de `account.move` y diagrama ERD).
- **Guía de Configuración**: [docs/development-guide.md](docs/development-guide.md) (Configuración de PostgreSQL y comandos de prueba).

---

## 🤝 Contribuciones

Al contribuir con mejoras a las reglas y estándares de este kit:
1. Actualice primero `docs/base-standards.md` (fuente única de verdad).
2. Pruebe los cambios con múltiples copilots de IA para garantizar la compatibilidad.
3. Suba sus cambios mediante ramas de características siguiendo el formato de commits de Odoo.

---

## 🙏 Agradecimientos y Créditos

Este repositorio ha sido desarrollado tomando inspiración y adaptando patrones de:
- El framework de desarrollo OpenSpec de [Fission AI](https://github.com/Fission-AI/OpenSpec).
- Los programas formativos de desarrollo con IA de [LIDR.co](https://lidr.co/ia-devs).
- El kit de herramientas y agentes de [Superpowers](https://github.com/obra/superpowers/tree/main), especialmente en los flujos de:
  - `using-git-worktrees`
  - `writing-skills`
- La habilidad de `odoo-code-auditing` está inspirada y adaptada de [jeffrigby/somepulp-agents](https://github.com/jeffrigby/somepulp-agents/tree/main).

**Hecho con 🤖 por el equipo de Focuz**

Para más información, dudas o sugerencias sobre desarrollo de software y automatizaciones asistidas por IA, visítenos en [focuz.io](https://focuz.io).

---

## 📄 Licencia

```text
Copyright (c) 2026 Focuz AI S.A.C.
Licensed under the MIT License
```
