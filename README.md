# Odoo Spec Kit: Desarrollo de Odoo Asistido por IA y OpenSpec

**odoo-spec-kit** es un kit de configuración y estándares técnicos portable diseñado para optimizar el desarrollo de módulos en **Odoo 18.0** (Community y Enterprise) mediante asistentes de Inteligencia Artificial (copilots como Claude, Cursor, Gemini/Antigravity y Copilot).

El kit establece un entorno unificado con foco inicial en **Contabilidad** (Accounting) y obliga a los agentes a adherirse estrictamente a las directrices oficiales de desarrollo y estilo de Odoo.

---

## 📋 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Estructura del Proyecto](#-estructura-del-proyecto)
3. [Inicio Rápido](#-inicio-rápido)
4. [Personalización Detallada](#-personalización-detallada)
5. [Configuración de OpenSpec (`config.yml`)](#-configuración-de-openspec-configyml)
6. [Workflow de Desarrollo OpenSpec](#-workflow-de-desarrollo-openspec)
7. [Habilidades de IA (Skills) Destacadas](#-habilidades-de-ia-skills-destacadas)
8. [Beneficios del Kit](#-beneficios-del-kit)
9. [Licencia](#-licencia)

---

## ✨ Características Principales

- **Multi-Copilot Ready**: Entry points y configuraciones nativas para Claude Code (`.claude`), Cursor (`.cursor`), y la CLI de Antigravity (`.agents`).
- **Estricto Español**: Toda la documentación técnica, comentarios, especificaciones de campos y mensajes de commit de Git se generan en español.
- **Spec-Driven Development (SDD)**: Enfoque de diseño técnico previo, estructurado en base al workflow de OpenSpec, con pruebas de verificación post-implementación.
- **Bucle de Autoreparación Autónomo**: La skill de `/code-review` ejecuta de forma autónoma hasta 3 intentos de corrección de código y pruebas si la validación del runner de Odoo falla.
- **Estándares Oficiales**: Síntesis integrada de las directrices oficiales de Odoo para Python, XML, JavaScript (OWL 2) y SCSS.

---

## 📂 Estructura del Proyecto

```text
odoo-spec-kit/
├── docs/                             # Contexto y directrices de ingeniería
│   ├── base-standards.md             # Reglas maestras (SDD, español, workflow)
│   ├── backend-standards.md          # Estándares ORM, Seguridad, SQL y XML views
│   ├── frontend-standards.md         # Componentes OWL 2, SCSS y HOOT testing
│   ├── coding-guidelines.md          # Directrices oficiales de código de Odoo
│   ├── git-guidelines.md             # Reglas y tags oficiales de commits de Odoo
│   ├── development-guide.md          # Guía de instalación y comandos odoo-bin
│   └── data-model.md                 # Modelo de datos contable de ejemplo
│   └── api-spec.md                   # Especificación de endpoints y controladores
│
├── ai-specs/
│   ├── agents/                       # Definiciones de agentes de IA
│   │   ├── odoo-module-developer.md  # Agente backend (Modelos, XML, Seguridad)
│   │   ├── odoo-owl-developer.md     # Agente frontend (OWL 2, QWeb, HOOT)
│   │   └── product-strategy-analyst.md # Analista funcional de producto Odoo
│   │
│   └── skills/                       # Skills de automatización (procesos)
│       ├── enrich-us/                # Enriquecimiento de requerimientos (Jira/Plane MCP)
│       ├── code-review/              # Revisión adversarial, seguridad estática y autoreparación
│       ├── commit-odoo/              # Creación de commits estilo Odoo y PRs con gh CLI
│       ├── code-auditing/            # Auditoría de calidad y linter de Odoo
│       ├── explain/                  # Mentoría conceptual de Odoo con quizzes
│       ├── odoo-scaffold/            # Generación de la estructura física de módulos
│       ├── odoo-test-runner/         # Formulación y ejecución de comandos de prueba
│       ├── sync-agent-symlinks/      # Sincronización de espejos (.claude, .cursor, .agents)
│       ├── update-docs/              # Actualización de documentación técnica
│       └── writing-skills/           # Metodología TDD para creación de nuevas skills
│
├── AGENTS.md, CLAUDE.md, GEMINI.md   # Accesos de copilots apuntando a base-standards
├── .ruff.toml                        # Configuración de linter Ruff para Python/Odoo
└── .pylintrc                         # Configuración de linter Pylint (pylint-odoo)
```

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

### 2) Importar el Kit en tu Proyecto

Copie todo el contenido de este repositorio en la raíz de su proyecto Odoo. Al importar, asegúrese de no sobreescribir archivos específicos del proyecto que ya existan (como el `README.md` original de su módulo):

```bash
# Copiar recursivamente sin sobreescribir (-n)
cp -rn odoo-spec-kit/* su-proyecto-odoo/
```

### 3) Configurar Enlaces de Agentes (Windows PowerShell)

Para que los diferentes entornos y editores de IA reconozcan las configuraciones de agentes y habilidades (skills), ejecute el siguiente comando desde una consola PowerShell con permisos para crear enlaces simbólicos (Junctions y Hardlinks):

```powershell
# Crear enlaces duros de configuración en la raíz
New-Item -ItemType HardLink -Path AGENTS.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path CLAUDE.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path GEMINI.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path codex.md -Value docs/base-standards.md -Force

# Crear Junctions de carpetas para los agentes y skills
New-Item -ItemType Junction -Path .claude/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .claude/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .cursor/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .cursor/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .agents/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .agents/skills -Value .\ai-specs\skills
```

---

## 🔧 Personalización Detallada

Para que el asistente de IA comprenda correctamente la arquitectura específica de su proyecto y no cometa errores de alucinación con modelos o dependencias inexistentes, es **obligatorio** adaptar la documentación técnica en `docs/`:

1. **Ajuste del Contexto de Negocio (`docs/base-standards.md`)**: Define si el idioma de tu empresa permite mezclar inglés en algunos campos o si es estrictamente en español.
2. **Definición de Base de Datos (`docs/data-model.md`)**: Reemplace el modelo de datos de ejemplo por la estructura física de sus tablas, campos y relaciones reales. Incorpore diagramas de flujo o de entidad-relación en Mermaid.
3. **Mapeo de Controladores (`docs/api-spec.md`)**: Si su módulo expone controladores HTTP o JSON-RPC, documente aquí las rutas exactas, parámetros y estructuras de respuesta JSON que deben respetar los desarrolladores de IA.
4. **Instalación y Entorno (`docs/development-guide.md`)**: Documente la ruta exacta de la base de datos de desarrollo y las dependencias del sistema operativo que requiere su módulo de Odoo.

---

## ⚙️ Configuración de OpenSpec (`config.yml`)

Después de inicializar OpenSpec e importar el kit, debe indicarle a OpenSpec cómo cargar y usar las reglas y agentes del proyecto. 

### Prompt para Automatizar con su Copiloto:
Envíe el siguiente prompt a su copilot para configurar de forma automática el archivo `config.yml`:

```text
Actualiza la sección context de mi archivo config.yml de OpenSpec para hacer referencia a la documentación y la estructura de ai-specs de este repositorio.

Requisitos:
- Usar docs/base-standards.md como la única fuente de verdad.
- Incluir docs/backend-standards.md, docs/frontend-standards.md y docs/documentation-standards.md.
- Incluir docs/api-spec.md y docs/data-model.md.
- Indicar al agente de IA que adopte ai-specs/agents/odoo-module-developer.md para tareas de backend y vistas XML, y ai-specs/agents/odoo-owl-developer.md para tareas de frontend OWL 2/SCSS.
- Indicar que utilice ai-specs/skills/ como guía de procesos y flujos de trabajo cuando aplique.
- Asegurar que todas las rutas sean relativas a la raíz del proyecto.
```

### Ejemplo de Estructura de `config.yml` Resultante:

```yaml
context: |
  Stack Tecnológico: Python 3.11, Odoo 18.0 (Community/Enterprise), PostgreSQL, OWL 2, SCSS.
  Arquitectura: Módulos Odoo extensibles mediante herencia (_inherit), MVC declarativo y OWL.
  Dominio: Localización contable de facturas y conciliaciones bancarias.
  Idioma Obligatorio: Español para todo el código, comentarios, commits y documentación.

  Estándares del Proyecto: La creación de artefactos y la implementación del código DEBEN seguir estrictamente el contexto técnico del repositorio en docs/. Lea y aplique los siguientes documentos antes de iniciar:
  - docs/base-standards.md — Principios Core (SDD, español, enlaces de copilots)
  - docs/backend-standards.md — Estándares ORM, Seguridad (SQL injection), y vistas XML
  - docs/frontend-standards.md — Estándares de componentes OWL 2, SCSS y HOOT testing
  - docs/api-spec.md — Rutas de controladores y contratos de API REST
  - docs/data-model.md — Modelos de datos del negocio contable
  - docs/documentation-standards.md — Reglas de documentación y mantenimiento

  Para la codificación:
  - Adopte el agente ai-specs/agents/odoo-module-developer.md para lógica de negocio en Python y vistas XML.
  - Adopte el agente ai-specs/agents/odoo-owl-developer.md para componentes de UI en JavaScript (OWL 2) y SCSS.
  - Utilice las guías de procesos y habilidades de ai-specs/skills/ como referencia del workflow.
```

---

## ✅ Verificación de la Configuración (Obligatorio)

Realice este paso de validación después de completar los pasos de configuración y setup descritos anteriormente.

Su copilot o agente de IA debería cargar automáticamente el archivo de configuración base al iniciar su sesión:

- **Claude CLI / Cursor**: Carga `CLAUDE.md` → Enlazado a `docs/base-standards.md`.
- **GitHub Copilot**: Carga `codex.md` → Enlazado a `docs/base-standards.md`.
- **Gemini**: Carga `GEMINI.md` → Enlazado a `docs/base-standards.md`.

Todas las rutas de directrices técnicas y las habilidades específicas de los agentes están mapeadas para funcionar correctamente y ser auto-cargadas sin necesidad de realizar ajustes manuales.

---

## 🔄 Workflow de Desarrollo OpenSpec

El kit impulsa un flujo de trabajo estructurado en base a las siguientes directivas de ejecución:

1. **`/enrich-us`**: Analiza y enriquece el requerimiento de negocio conectándose a Jira o Plane MCP, y buscando de forma obligatoria en el código real de Odoo en lugar de adivinar nombres de campos.
2. **`/propose`**: Diseña la especificación técnica en markdown detallando modelos, campos, lógica de negocio y pruebas.
3. **`/apply`**: Escribe el código fuente de forma incremental.
4. **`/verify` + `/code-review`**:
   - `/verify` ejecuta las pruebas nativas de Odoo (`odoo-bin --test-enable`).
   - `/code-review` ejecuta la auditoría estática de seguridad, valida accesos y activa el **Bucle de Autoreparación** si hay fallos en las pruebas.
5. **`/archive` + `/commit-odoo`**: Archiva el ciclo de cambios y empaqueta el commit con el formato oficial de Odoo (ej. `[ADD] mi_modulo: agregar facturación local`).

### 💡 Ejemplo: Flujo de Extremo a Extremo (End-to-End)

Ejecute estos comandos en secuencia para desarrollar una tarea:

*Paso inicial opcional (recomendado): Crear un entorno aislado utilizando la skill de git worktrees antes de arrancar.*

```bash
/enrich-us TICKET-101
/propose TICKET-101
/apply TICKET-101
/verify TICKET-101
/code-review TICKET-101
/archive TICKET-101
/commit-odoo
```

Los artefactos se gestionan y guardan a través de las carpetas de OpenSpec durante este flujo, incluyendo los reportes de pruebas unitarias y de revisión adversarial de seguridad.

---

## 🛠️ Habilidades de IA (Skills) Destacadas

Las habilidades del kit residen en `ai-specs/skills/` y guían al agente en tareas comunes:

- **`enrich-us`**: Enriquecimiento de historias de usuario con control estricto de no-adivinación de esquemas y conexión MCP.
- **`code-review`**: Auditoría pre-merge de calidad y seguridad Odoo + Bucle autónomo de Autoreparación ante tracebacks.
- **`commit-odoo`**: Valida y formatea mensajes de commit bajo los tags oficiales de Odoo (`[ADD]`, `[FIX]`, `[IMP]`, etc.) y crea la PR.
- **`code-auditing`**: Metodología sistemática de 6 fases para detectar código muerto, antipatrones ORM, inyecciones SQL y deuda técnica.
- **`odoo-scaffold`**: Creación de la estructura física estándar de nuevos addons de Odoo con manifiestos LGPL y plantillas CSV.
- **`odoo-test-runner`**: Ayuda a formular comandos optimizados con `--test-tags` y a extraer tracebacks limpios para la IA.

---

## 🎯 Beneficios del Kit

- **Calidad de Código Consistente**: La IA genera vistas XPath estables y consultas seguras sin desviación de estilo.
- **Seguridad Garantizada**: Análisis adversarial automático de inyecciones SQL (uso obligado de `odoo.tools.SQL`) y validación de accesos CSV en cada cambio.
- **Menos Bloqueos**: El bucle de autoreparación resuelve de forma autónoma tracebacks de compilación o fallos sencillos de aserciones de pruebas.
- **Documentación Siempre Viva**: Los modelos de datos contables y especificaciones de APIs se mantienen sincronizados con los cambios de código.

---

## 🙏 Agradecimientos y Créditos

Este repositorio ha sido desarrollado tomando inspiración y adaptando patrones de:
- El framework de desarrollo OpenSpec de [Fission AI](https://github.com/Fission-AI/OpenSpec).
- Los programas formativos de desarrollo con IA de [LIDR.co](https://lidr.co/ia-devs).
- El kit de herramientas y agentes de [Superpowers](https://github.com/obra/superpowers/tree/main), especialmente en los flujos de:
  - `using-git-worktrees`
  - `writing-skills`
- La habilidad de `code-auditing` está inspirada y adaptada de [jeffrigby/somepulp-agents](https://github.com/jeffrigby/somepulp-agents/tree/main).

**Hecho con 🤖 por el equipo de Focuz**

Para más información, dudas o sugerencias sobre desarrollo de software y automatizaciones asistidas por IA, visítenos en [focuz.io](https://focuz.io).

---

## 📄 Licencia

```text
Copyright (c) 2026 Focuz AI S.A.C.
Licensed under the MIT License
```
