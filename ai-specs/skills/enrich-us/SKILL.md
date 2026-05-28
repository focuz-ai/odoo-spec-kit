---
name: enrich-us
description:
  Analiza y enriquece historias de usuario con detalles técnicos completos y listos para implementación en Odoo EE
  siguiendo el Spec-Driven Development.
author: Focuz.io
version: 1.4.0
---

# Skill enrich-us

Úsalo cuando se requiera este flujo de trabajo en el proyecto para refinar y enriquecer una Historia de Usuario (User
Story) antes de su implementación.

## Instrucciones

Por favor, analiza y enriquece el siguiente ticket: $ARGUMENTS.

Sigue estos pasos:

1. Determina la fuente de entrada del ticket:
   - **Modo de entrada directa (por defecto cuando se proporciona el texto del ticket):** Usa el contenido del ticket
     compartido por el usuario en el prompt/chat.
   - **Modo Jira/Plane (opcional):** Si el usuario proporciona un ID/clave de incidencia o pide usar una herramienta de
     gestión de proyectos, intenta usar **Jira MCP** primero para obtener los detalles del ticket. Si Jira no está
     configurado o falla, usa **Plane MCP** como alternativa para recuperar el ítem de trabajo.
2. Actúa como un **Product Manager** y un **Arquitecto Técnico de Odoo EE** experto en Spec-Driven Development (SDD).
3. **Manejo de Rutas Locales (Community/Enterprise):** Lee el archivo `config/local.paths.json` para identificar las
   rutas del código base utilizando explícitamente las variables `odoo_community_root` y, si aplica,
   `odoo_enterprise_root` (opcional). Si este archivo no existe, extrae la variable `addons_path` del archivo
   `odoo.conf` del proyecto. Esto es crucial para saber dónde buscar referencias correctas y dónde ubicar los nuevos
   desarrollos.
4. **Búsqueda de Contexto Real:** Antes de proponer una arquitectura técnica, utiliza tus herramientas de solo lectura
   para buscar activamente en el código fuente actual utilizando las rutas identificadas. Verifica la existencia de
   módulos base, vistas heredadas y lógica de negocio actual relacionada con el ticket para evitar alucinar estructuras
   o dependencias.
5. **Validación de Funcionalidad Nativa (No reinventar la rueda):** Odoo es un ERP sumamente extenso. Antes de proponer
   un desarrollo personalizado, evalúa y busca en el código base (Community/Enterprise) si la funcionalidad solicitada
   ya existe nativamente. Si la necesidad se puede cubrir instalando un módulo estándar o mediante configuraciones
   existentes, la propuesta debe enfocarse en la **configuración/instalación** en lugar de en el desarrollo de código.
6. Entiende el problema descrito en el ticket, siguiendo el principio de _Anti-Vibe-Coding_ (diseñar antes de
   programar). Asegúrate de que el valor de negocio, los flujos de usuario y los casos extremos (edge cases) estén
   claramente identificados desde una perspectiva de Product Management.
7. **Validación de Completitud Técnica (Específica por Versión):** Decide si la Historia de Usuario está completamente
   detallada de acuerdo con las mejores prácticas de Odoo para la **versión específica de Odoo** utilizada en el
   proyecto (ej. Odoo). Valida que incluya:
   - Descripción completa de la funcionalidad y reglas de negocio.
   - **Modelos de Datos (ORM):** Nuevos modelos, campos, relaciones (`Many2one`, etc.), campos calculados (computes) y
     restricciones (constraints) válidos para la versión objetivo. _(Solo si requiere desarrollo)._
   - **Vistas y UI:** Herencia de vistas (XPath), Form, Tree, Kanban, Menús y Acciones compatibles con el frontend de la
     versión objetivo (ej. OWL 2 / legacy QWeb para Odoo 16+). _(Solo si requiere desarrollo)._
   - **Seguridad:** Grupos de seguridad (`res.groups`), Derechos de Acceso (`ir.model.access.csv`) y Reglas de Registro
     (`ir.rule`).
   - **Lógica de Negocio:** Wizards, sobreescritura de métodos estándar (`create`, `write`) o Acciones de Servidor.
     _(Solo si requiere desarrollo)._
   - **Mejores Prácticas de Odoo:** Consideraciones técnicas para la versión específica (ej. evitar N+1 queries, uso
     correcto de `@api.depends`, reutilización de módulos estándar de Odoo).
   - Definición de Hecho (DoD - pasos de implementación y entrega).
8. Si la historia carece del detalle técnico suficiente para una implementación autónoma, proporciona una versión
   mejorada que sea más clara, específica y concisa, alineada con los pasos 6 y 7. Usa el contexto técnico del proyecto
   desde `@documentation`.
9. **Estándares de Idioma:** Asegúrate de que todo el texto descriptivo, reglas de negocio y contexto estén escritos en
   **Español**, pero mantén estrictamente todos los nombres técnicos (modelos, campos, métodos, IDs de XML) en
   **Inglés**.
10. El formato de salida debe incluir siempre la siguiente estructura en markdown:
    - `## Original`
    - `## Enhanced (Odoo Spec)`
      - `### 1. Contexto y Reglas de Negocio (Visión de Producto)`
      - `### 2. Arquitectura de Modelos (ORM) o Configuración Nativa`
      - `### 3. Vistas y UI (XML/OWL - Específico por versión)`
      - `### 4. Seguridad y Control de Accesos`
      - `### 5. Lógica de Negocio (Python/Wizards)`
      - `### 6. Consideraciones Técnicas (Rutas de Módulos y Odoo Best Practices)`
      - `### 7. Criterios de Aceptación (DoD)`
11. La reescritura en la herramienta de Project Management es opcional y solo aplica en modo Jira/Plane:
    - Actualiza el ticket agregando el contenido enriquecido después del contenido original, con secciones `h2` claras
      `[original]` y `[enhanced]` y un formato legible (listas/bloques de código cuando sea útil).
    - Si el estado del ticket es `To refine` (o equivalente en Plane), muévelo a `Pending refinement validation`.

## Notas

- No exijas Jira/Plane cuando el usuario ya haya proporcionado el contenido completo del ticket directamente.
- Si la entrada es ambigua (por ejemplo, el usuario da una referencia corta sin contenido), pregunta si debe resolverse
  mediante herramientas externas (Jira/Plane) o solicita el texto completo del ticket.
