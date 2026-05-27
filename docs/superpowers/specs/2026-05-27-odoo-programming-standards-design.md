# Especificación de Diseño: Implementación de Estándares de Programación (Odoo 16.0)

Este documento especifica la integración de los estándares de programación modernos de
la OCA en el kit de configuración portable **Odoo Spec Kit**, asegurando compatibilidad
nativa con Odoo Community y Odoo Enterprise 16.0.

## 1. Contexto y Objetivos

El objetivo principal es dotar a este repositorio de estándares de programación
actualizados que puedan ser utilizados por copilotos de IA y desarrolladores. Para ello,
adaptamos la suite de herramientas modernas de la OCA (especialmente Ruff y Prettier con
plugins XML) que se encuentran en Odoo 18.0, pero asegurando su compatibilidad con
entornos de ejecución de Odoo 16.0 y licencias de Odoo Enterprise.

## 2. Especificación de los Archivos de Configuración

### 2.1 `.pre-commit-config.yaml`

Establece la pipeline de verificación estática local. Se elimina el uso redundante de
`black`, `isort` y `flake8` para delegar el formateado e inspección de estilo en Ruff.

**Características principales:**

- **Ruff (`v0.6.8`)**: Ejecuta `ruff` con autofix y `ruff-format` para formateo rápido.
- **Prettier (`v3.3.3`)**: Emplea el plugin `@prettier/plugin-xml@3.4.1` para indentar
  correctamente vistas XML de Odoo sin dependencias globales de Node.
- **Pylint con `pylint-odoo`**: Corre inspecciones específicas de Odoo. Se separa en:
  - `.pylintrc` (informa advertencias y sugerencias generales de desarrollo sin bloquear
    el commit).
  - `.pylintrc-mandatory` (evalúa reglas de seguridad y sintaxis críticas; bloquea el
    commit ante fallos).

### 2.2 `.ruff.toml`

Controla el comportamiento del formateador y linter Ruff.

- **Versión objetivo**: `target-version = "py310"` para asegurar compatibilidad con
  Python 3.10 de Odoo 16.0.
- **Reglas del Linter**:
  - Habilita `B` (Bugbear), `C90` (mccabe), `I` (isort) y `UP` (pyupgrade).
  - Excluye explícitamente directorios de empaquetado o setups (`setup/*`).
- **Imports (`isort`)**: Mapea secciones dedicadas para `odoo` y `odoo.addons` para
  estructurar los imports según la convención oficial.

### 2.3 `prettier.config.cjs`

Configura las reglas de estilo de Prettier usando CommonJS:

- Integra `@prettier/plugin-xml` localmente.
- Configura `printWidth: 88`, `proseWrap: "always"`, y
  `xmlWhitespaceSensitivity: "preserve"`.

### 2.4 `.pylintrc` y `.pylintrc-mandatory`

Ambos heredan el conjunto completo de mensajes habilitados de la OCA v16.0.

- **Compatibilidad con Odoo Enterprise**:
  - Se añade `OEEL-1` (Odoo Enterprise Edition License) y `OPL-1` (Odoo Proprietary
    License) a la lista `license-allowed` para prevenir advertencias de licencia no
    válida en módulos Enterprise.
  - Se añade `Odoo S.A.` a la lista de autores permitidos (`manifest-required-authors`)
    junto con `Odoo Community Association (OCA)` y `Focuz AI`.

## 3. Plan de Verificación

Para garantizar que los archivos implementados funcionan correctamente, realizaremos
pruebas sintácticas usando las herramientas instaladas de pre-commit y validaremos la
conformidad del formateador con archivos de ejemplo tanto de código libre como de código
Enterprise.
