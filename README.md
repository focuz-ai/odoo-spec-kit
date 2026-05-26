# Odoo Spec Kit: Desarrollo de Odoo Asistido por IA y OpenSpec

**odoo-spec-kit** es un kit de configuración y estándares técnicos portable diseñado para acelerar y dar rigurosidad al desarrollo de módulos en **Odoo 18.0** (Community y Enterprise). Utiliza asistentes de Inteligencia Artificial (copilots como Claude, Cursor, Gemini/Antigravity y Copilot) estructurados mediante la metodología **Spec-Driven Development (SDD)**.

Este kit proporciona a las IAs el contexto del ORM de Odoo, las guías de estilo oficiales, y un flujo de trabajo estructurado para garantizar entregas limpias, testeadas y seguras, con foco inicial en **Contabilidad** (Accounting).

---

## 📁 Estructura del Repositorio

```text
.
├── docs/                             # Contexto técnico y estándares de ingeniería
│   ├── base-standards.md             # Reglas maestras (SDD, español, workflow)
│   ├── backend-standards.md          # Estándares ORM, Seguridad, SQL y XML views
│   ├── frontend-standards.md         # Componentes OWL 2, SCSS y HOOT testing
│   ├── coding-guidelines.md          # Directrices oficiales de código de Odoo
│   ├── git-guidelines.md             # Reglas y tags oficiales de commits de Odoo
│   ├── development-guide.md          # Guía de instalación y comandos odoo-bin
│   ├── data-model.md                 # Modelo de datos contable de ejemplo
│   └── api-spec.md                   # Especificación de endpoints y controladores
│
├── ai-specs/
│   ├── agents/                       # Definiciones de roles de agentes de IA
│   │   ├── odoo-module-developer.md  # Agente backend (Modelos, XML, Seguridad)
│   │   ├── odoo-owl-developer.md     # Agente frontend (OWL 2, QWeb, HOOT)
│   │   └── product-strategy-analyst.md # Analista funcional de producto Odoo
│   │
│   └── skills/                       # Habilidades y flujos reutilizables (skills)
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

## 🤖 Soporte Multi-Copiloto

Este repositorio utiliza **enlaces duros (hardlinks)** y **uniones de directorio (junctions)** para dar soporte a múltiples copilots de IA sin duplicar archivos en el espacio de trabajo:

- **`AGENTS.md`** → Reglas genéricas de agentes.
- **`CLAUDE.md`** → Configuración para Claude Code / Claude CLI.
- **`GEMINI.md`** → Configuración para Google Gemini.
- **`codex.md`** → Configuración para GitHub Copilot.

Todos estos archivos de la raíz apuntan a la misma fuente de verdad en `docs/base-standards.md`. Cualquier actualización de las directrices impacta instantáneamente a todos los copilots.

---

## 🚀 Guía Rápida de Setup

### 1. Clonar o copiar el kit en su proyecto Odoo
Copie el contenido de este repositorio en la raíz de su espacio de trabajo de Odoo.

```bash
# Copiar recursivamente sin sobreescribir el README original del proyecto
cp -rn odoo-spec-kit/* su-proyecto-odoo/
```

### 2. Crear los Enlaces del Kit (Windows PowerShell)
Ejecute el siguiente bloque en una terminal PowerShell para enlazar las configuraciones de los copilots y editores a las carpetas canónicas en `ai-specs/`:

```powershell
# Enlaces duros de configuración en la raíz
New-Item -ItemType HardLink -Path AGENTS.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path CLAUDE.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path GEMINI.md -Value docs/base-standards.md -Force
New-Item -ItemType HardLink -Path codex.md -Value docs/base-standards.md -Force

# Uniones de directorio (Junctions) para copilots
New-Item -ItemType Junction -Path .claude/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .claude/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .cursor/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .cursor/skills -Value .\ai-specs\skills
New-Item -ItemType Junction -Path .agents/agents -Value .\ai-specs\agents
New-Item -ItemType Junction -Path .agents/skills -Value .\ai-specs\skills
```

### 3. Personalizar la documentación
Modifique los archivos de la carpeta `docs/` con el contexto técnico real de su proyecto (base de datos de desarrollo, módulos personalizados, dependencias de Odoo, flujos contables y localizaciones requeridas).

### 4. Apuntar la configuración de OpenSpec (`config.yml`)
Si utiliza OpenSpec, configure su archivo `config.yml` para vincular el contexto y las reglas globales a este kit:

```yaml
context: |
  Stack Tecnológico: Python 3.11, Odoo 18.0, PostgreSQL, OWL 2, SCSS, Ruff.
  Dominio: Localización y personalizaciones contables (account.move, account.tax).
  Idioma Obligatorio: Español para todo el código, comentarios, commits y documentación.

  Reglas de Proyecto: Toda la implementación debe seguir los estándares técnicos descritos en:
  - docs/base-standards.md — Principios de desarrollo e idioma
  - docs/backend-standards.md — Estándares de ORM, Seguridad y vistas XML de Odoo
  - docs/frontend-standards.md — Componentes OWL 2 y HOOT testing
  - docs/coding-guidelines.md — Odoo Coding Guidelines oficiales
  
  Para la ejecución, adopte el agente de ai-specs/agents/ correspondiente.

rules:
  _global:
    - Antes de comenzar, lea y aplique docs/base-standards.md.
    - Para cambios en backend o vistas XML, adopte ai-specs/agents/odoo-module-developer.md.
    - Para cambios en OWL 2 o SCSS, adopte ai-specs/agents/odoo-owl-developer.md.
```

---

## 🔄 Workflow de Desarrollo OpenSpec

El desarrollo utilizando **odoo-spec-kit** sigue un ciclo de vida estrictamente verificado:

1. **`/enrich-us`**: Enriquece requerimientos ambiguos usando Plane/Jira MCP, validando de forma obligatoria en el código fuente de Odoo o en la base de datos en lugar de adivinar nombres de campos.
2. **`/propose`**: Genera la especificación técnica (diseño técnico de modelos, vistas XML, seguridad y estrategia de pruebas).
3. **`/apply`**: Escribe el código Python/XML/JS de forma incremental.
4. **`/verify`**: Ejecuta las pruebas de Odoo nativas (`odoo-bin --test-enable`) mediante la herramienta de ejecución de terminal.
5. **`/code-review`**: Realiza la auditoría adversarial de seguridad (inyección SQL con `odoo.tools.SQL`, record rules y accesos CSV) y ejecuta de forma autónoma el **Bucle de Autoreparación** (hasta 3 intentos de corrección del código) si `/verify` falla.
6. **`/archive`**: Archiva el ciclo de cambios.
7. **`/commit-odoo`**: Genera el commit Git siguiendo el formato oficial de Odoo (ej. `[FIX] account: corregir validación de impuestos`) y abre el Pull Request en GitHub mediante `gh` CLI.

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

## 🎯 Beneficios

### Para Desarrolladores
- **Calidad Consistente**: La IA genera vistas XPath estables y consultas seguras sin desviación de estilo.
- **Seguridad Garantizada**: Análisis adversarial automático de inyecciones SQL y permisos CSV en cada cambio.
- **Menos Bloqueos**: El bucle de autoreparación resuelve de forma autónoma tracebacks de compilación o fallos sencillos de aserciones.

### Para el Proyecto
- **Reducción de Deuda Técnica**: Estándares de estructuración (Think Extendable) forzados desde el día uno.
- **Documentación Viva**: Modelos de datos contables y especificaciones de APIs siempre sincronizados con los cambios de código.
- **Robustez**: Mayor cobertura de pruebas unitarias y tours de integración ejecutados localmente antes de cada integración.

---

## 🤝 Créditos y Agradecimientos

Este repositorio ha sido desarrollado tomando inspiración y adaptando patrones de:
- El framework de desarrollo OpenSpec de [Fission AI](https://github.com/Fission-AI/OpenSpec).
- Los programas de formación de desarrollo con IA de [LIDR.co](https://lidr.co/ia-devs).
- El kit de herramientas y agentes de [Superpowers](https://github.com/obra/superpowers).
