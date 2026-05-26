# Odoo Spec Kit — Kit de Desarrollo Asistido por IA en Odoo 18.0

**odoo-spec-kit** es un kit de configuración y estándares técnicos portable diseñado para optimizar el desarrollo de módulos en **Odoo 18.0** (Community y Enterprise) mediante asistentes de Inteligencia Artificial (copilots como Claude, Cursor, Gemini/Antigravity y Copilot).

El kit establece un entorno unificado con foco inicial en **Contabilidad** (Accounting) y obliga a los agentes a adherirse estrictamente a las directrices oficiales de desarrollo y estilo de Odoo.

---

## 📋 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Estructura del Proyecto](#-estructura-del-proyecto)
3. [Instalación y Configuración Rápida](#-instalación-y-configuración-rápida)
4. [Workflow de Desarrollo OpenSpec](#-workflow-de-desarrollo-openspec)
5. [Directrices y Reglas de Idioma](#-directrices-y-reglas-de-idioma)
6. [Licencia](#-licencia)

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
│       ├── code-auditing/            # Auditoría sistemática de calidad y linter de Odoo
│       ├── explain/                  # Mentoría conceptual de Odoo con quizzes interactivos
│       ├── odoo-scaffold/            # Generación del andamiaje físico de nuevos módulos
│       ├── odoo-test-runner/         # Formulación y ejecución de comandos de prueba
│       ├── sync-agent-symlinks/      # Sincronización de espejos (.claude, .cursor, .agents)
│       ├── update-docs/              # Actualización de documentación técnica según cambios
│       └── writing-skills/           # Metodología TDD para creación de nuevas skills
│
├── AGENTS.md, CLAUDE.md, GEMINI.md   # Accesos de copilots apuntando a base-standards
├── .ruff.toml                        # Configuración de linter Ruff para Python/Odoo
└── .pylintrc                         # Configuración de linter Pylint (pylint-odoo)
```

---

## 🚀 Instalación y Configuración Rápida

Para utilizar este kit en cualquier repositorio de desarrollo de Odoo:

### 1. Copiar el kit
Copie todo el contenido de `odoo-spec-kit/` en la raíz de su repositorio o espacio de trabajo de Odoo.

### 2. Configurar Enlaces de Agentes (Junctions y Hardlinks)
En sistemas Windows, ejecute el siguiente comando desde una consola PowerShell para inicializar los entry points de los editores y copilots:

```powershell
# Crear enlaces duros de configuración en la raíz
New-Item -ItemType HardLink -Path AGENTS.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path CLAUDE.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path GEMINI.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path codex.md -Value docs/base-standards.md -Force

# Crear Junctions de carpetas para los agentes
New-Item -ItemType Junction -Path .claude/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .claude/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .cursor/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .cursor/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .agents/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .agents/skills -Value .\ai-specs\skills
```

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

---

## ✍️ Directrices y Reglas de Idioma

- **Idioma**: El idioma oficial para el desarrollo técnico de este proyecto es el **Español**. Toda documentación, comentarios del código Python y XML, y nombres de métodos del negocio deben estar en español.
- **Commits**: Los mensajes de commit se escriben en español, utilizando únicamente terminología de Odoo en inglés para los tags de cabecera (`[FIX]`, `[ADD]`, `[IMP]`).
- **Seguridad**: Está estrictamente prohibido usar concatenaciones strings en queries directos a base de datos. Utilice siempre `odoo.tools.SQL`.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulte el archivo `LICENSE` para más detalles.
