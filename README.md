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
│   └── api-spec.md                   # Especificación de endpoints y controladores
│
├── ai-specs/
│   ├── agents/                       # Definiciones de roles de agentes de IA
│   │   ├── odoo-module-developer.md  # Agente backend (Modelos, XML, Seguridad)
│   │   ├── odoo-owl-developer.md     # Agente frontend (OWL 2, QWeb, QUnit)
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

Este repositorio utiliza **enlaces simbólicos (symlinks)** y **convenciones de nombres** para dar soporte a múltiples copilots de IA de forma nativa sin duplicar archivos en el espacio de trabajo:

- **`AGENTS.md`** → Reglas genéricas de agentes (compatible con la mayoría de copilots).
- **`CLAUDE.md`** → Optimizado para Claude/Cursor.
- **`GEMINI.md`** → Optimizado para Google Gemini.
- **`codex.md`** → Optimizado para GitHub Copilot / Codex.

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

### 2) Importar el Kit en tu Proyecto

Copie todo el contenido de este repositorio en la raíz de su proyecto Odoo. Al importar, asegúrese de no sobreescribir archivos específicos del proyecto que ya existan (como el `README.md` original de su módulo):

```bash
# Copiar recursivamente sin sobreescribir (--ignore-existing)
rsync -a --ignore-existing odoo-spec-kit/ su-proyecto-odoo/
```

### 3) Personalizar `docs/` para tu Proyecto (Obligatorio)

Este paso es obligatorio. Si lo omite, su asistente de IA utilizará contexto técnico genérico en lugar del contexto de su proyecto real.

Actualice los archivos en `docs/` para que coincidan con su base de datos de desarrollo, módulos personalizados, dependencias de Odoo, flujos contables y localizaciones requeridas. Consulte la sección [Personalización](#-personalización) para obtener instrucciones detalladas.

### 4) Apuntar la Configuración de OpenSpec a `docs/` y `ai-specs/`

Después de inicializar OpenSpec e importar el kit, debe indicarle a OpenSpec cómo cargar y usar las reglas y agentes del proyecto. Envíe el siguiente prompt a su copilot para configurar de forma automática el archivo `config.yml`:

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

---

## ✅ Verificación de la Configuración (Obligatorio)

Realice este paso de validación después de completar los pasos de configuración y setup descritos anteriormente. Su copilot o agente de IA debería cargar automáticamente el archivo de configuración base al iniciar su sesión:

- **Claude CLI / Cursor**: Carga `CLAUDE.md` → Enlazado a `docs/base-standards.md`.
- **GitHub Copilot**: Carga `codex.md` → Enlazado a `docs/base-standards.md`.
- **Gemini**: Carga `GEMINI.md` → Enlazado a `docs/base-standards.md`.

Todas las rutas de directrices técnicas y las habilidades específicas de los agentes están mapeadas para funcionar correctamente y ser auto-cargadas sin necesidad de realizar ajustes manuales en los editores.

---

## 💡 Uso: Workflow Oficial de OpenSpec

El desarrollo utilizando **odoo-spec-kit** sigue un ciclo de vida estrictamente verificado:

1. **`/enrich-us`**: Analiza y enriquece el requerimiento de negocio conectándose a Jira o Plane MCP, y buscando de forma obligatoria en el código real de Odoo en lugar de adivinar nombres de campos.
2. **`/propose`**: Diseña la especificación técnica en markdown detallando modelos, campos, lógica de negocio y pruebas.
3. **`/apply`**: Escribe el código fuente de forma incremental.
4. **`/verify` + `/code-review`**:
   - `/verify` ejecuta las pruebas nativas de Odoo (`odoo-bin --test-enable`).
   - `/code-review` ejecuta la auditoría estática de seguridad, valida accesos y activa el **Bucle de Autoreparación** si hay fallos en las pruebas.
5. **`/archive`**: Archiva el ciclo de cambios.
6. **`/commit-odoo`**: Archiva el ciclo de cambios y empaqueta el commit con el formato oficial de Odoo (ej. `[ADD] mi_modulo: agregar facturación local`).

### Opcional: Integraciones MCP (Jira + Plane)

Este flujo de trabajo se ve reforzado con servidores de Protocolo de Contexto de Modelo (MCP) integrados en el flujo. Estos son opcionales y pueden omitirse o reemplazarse por herramientas equivalentes:

- **Jira MCP / Plane MCP (recomendados en `/enrich-us`)**: Permiten al agente leer directamente los tickets desde sus tableros de gestión para enriquecer las historias de usuario sin necesidad de copiar y pegar manualmente.

### Ejemplo: Flujo de Extremo a Extremo (End-to-End)

Ejecute estos comandos en secuencia para desarrollar una tarea:

*Paso inicial opcional (recomendado): Crear una rama aislada utilizando la skill de git worktrees antes de arrancar.*

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

### Habilidades (Skills) Útiles

Las habilidades del kit residen en `ai-specs/skills/` y se vinculan a `.claude/skills/` y `.cursor/skills/` para facilitar su descubrimiento:

- **`enrich-us`** — Convierte requerimientos ambiguos de Jira o Plane en especificaciones técnicas de Odoo detallando modelos, campos y XPath XML.
- **`code-review`** — Auditoría pre-merge de calidad y seguridad Odoo + Bucle autónomo de Autoreparación de 3 intentos ante tracebacks.
- **`commit-odoo`** — Valida y formatea mensajes de commit bajo los tags oficiales de Odoo (`[ADD]`, `[FIX]`, `[IMP]`, etc.) y crea la PR.
- **`code-auditing`** — Metodología sistemática de 6 fases para detectar código muerto, antipatrones ORM, inyecciones SQL y deuda técnica.
- **`odoo-scaffold`** — Creación de la estructura física estándar de nuevos addons de Odoo con manifiestos LGPL y plantillas CSV.
- **`odoo-test-runner`** — Ayuda a formular comandos optimizados con `--test-tags` y a extraer tracebacks limpios para la IA.
- **`explain`** — Mentoría conceptual interactiva sobre el ORM, OWL, seguridad y contabilidad de Odoo mediante preguntas y respuestas.
- **`update-docs`** — Identifica y actualiza la documentación técnica en `docs/` de acuerdo con los cambios de código aplicados.
- **`sync-agent-symlinks`** — Sincroniza y mantiene la integridad de los enlaces y junctions del kit.
- **`writing-skills`** — Guía metodológica en TDD para la creación de nuevas habilidades para los copilots.

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
Siguiendo la misma estructura base presente en docs/, actualiza todos los documentos de contexto técnico según las especificaciones de este proyecto.

Requisitos:
- Mantener los mismos nombres de archivos en docs/.
- Reemplazar el contenido genérico con los datos reales de la base de datos de desarrollo, módulos personalizados, dependencias de Odoo y localizaciones de este proyecto.
- Actualizar los estándares de backend y frontend para reflejar las prácticas de este equipo.
- Asegurar que todas las referencias sean coherentes internamente y se redacten en español.
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
- La habilidad de `code-auditing` está inspirada y adaptada de [jeffrigby/somepulp-agents](https://github.com/jeffrigby/somepulp-agents/tree/main).

**Hecho con 🤖 por el equipo de Focuz**

Para más información, dudas o sugerencias sobre desarrollo de software y automatizaciones asistidas por IA, visítenos en [focuz.io](https://focuz.io).

---

## 📄 Licencia

```text
Copyright (c) 2026 Focuz AI S.A.C.
Licensed under the MIT License
```
