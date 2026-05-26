---
description: Estándares y mejores prácticas para la documentación técnica y las especificaciones de IA en odoo-spec-kit, incluyendo reglas de idioma, triggers de actualización y auto-mejora.
alwaysApply: true
---

# Reglas y Patrones de Documentación y Especificaciones de IA (Documentation Standards)

## 1. Introducción

Este documento define las directrices obligatorias para la creación, mantenimiento y actualización de la documentación técnica y las especificaciones de comportamiento para agentes de IA dentro de proyectos Odoo.

- **Documentación Técnica**: READMEs, especificaciones de modelos de datos, guías de instalación, esquemas de APIs/controladores y descripciones estáticas de módulos (`static/description/`).
- **Especificaciones de IA**: Reglas de desarrollo, prompts de agentes, instrucciones de skills y configuraciones que guían el comportamiento de los copilots (Claude, Cursor, Gemini, etc.).

---

## 2. Regla de Idioma: Documentación y Código

> [!IMPORTANT]
> **La documentación y los artefactos de OpenSpec se escriben exclusivamente en Español, mientras que toda la programación y código fuente se escribe estrictamente en Inglés.**
>
> **En Español (Documentación y Especificaciones):**
> - Archivos de especificación técnica de OpenSpec (historias de usuario, especificaciones de diseño, planes de implementación, walkthroughs y `tasks.md`).
> - README del repositorio y guías de instalación.
>
> **En Inglés (Toda la Programación):**
> - Todo el código fuente de programación (Python, JavaScript, XML, CSV).
> - Comentarios dentro del código, nombres de variables, funciones, clases y métodos.
> - Mensajes de error técnicos, logs, descripciones de campos de modelos de Odoo (`string="..."`, `help="..."`).
> - Archivo de manifiesto de Odoo (`__manifest__.py`), incluyendo el sumario y descripción.
> - Commits de Git y descripciones de Pull Requests.

---

## 3. Documentación Técnica de Módulos Odoo

Antes de finalizar cualquier tarea o realizar un commit/push, el agente debe revisar y actualizar la documentación técnica del módulo si se han modificado los siguientes elementos:

| Cambio Realizado | Acción de Documentación Requerida |
|---|---|
| **Nuevo modelo o campo** | Actualizar `docs/data-model.md` con la nueva estructura de campos y relaciones. Agregar comentarios detallados (`help="..."`) en el código Python del campo. |
| **Nuevo Controller / Ruta** | Documentar el endpoint en `docs/api-spec.md` con los parámetros esperados, respuestas y modo de autenticación. |
| **Cambio de dependencia** | Actualizar el archivo `__manifest__.py` y reflejar el cambio en la guía de instalación (`docs/development-guide.md`) si requiere librerías del sistema. |
| **Actualización de Seguridad** | Documentar nuevos grupos, accesos CSV o reglas de registro (`record rules`) en el archivo correspondiente. |

### Documentación Estándar de un Módulo Odoo:
Cada módulo Odoo debe incluir un archivo informativo en su raíz o en `static/description/index.html` para explicar visualmente sus funciones y configuración al usuario final de Odoo.

---

## 4. Estándares para Especificaciones de IA y Auto-Mejora

Los agentes de IA deben aprender continuamente de las interacciones y el feedback del usuario humano para refinar de forma proactiva estas reglas.

### Proceso de Aprendizaje y Actualización de Reglas:
1. **Detección de Oportunidades**: Identificar correcciones de código repetitivas, preferencias del usuario o patrones no contemplados en las reglas existentes.
2. **Propuesta Quirúrgica**: Si una regla de desarrollo debe modificarse, el agente debe proponer el cambio de forma quirúrgica en `docs/base-standards.md` o el archivo de estándares específico, especificando qué secciones cambian.
3. **Aprobación del Usuario**: Nunca modifique las reglas centrales del proyecto de forma directa sin antes presentar la propuesta y obtener la aprobación explícita en el workflow.
4. **Confirmación**: Una vez aprobado, aplicar el cambio y confirmar su aplicación al usuario antes de proceder con el código.

### Antipatrones a Evitar por la IA:
- **Anti-Vibe-Coding / Omitir Fase de Diseño**: Escribir código inmediatamente al recibir una historia de usuario o requerimiento de negocio sin haber creado y obtenido aprobación previa de la propuesta de diseño y planificación correspondientes (`proposal.md`, `design.md`, `tasks.md`).
- **Ignorar el Idioma**: Escribir comentarios, nombres de variables o código fuente en español, o redactar especificaciones, planes y documentación técnica externa en inglés.
- **Falta de Trazabilidad**: Cambiar directrices de desarrollo de forma proactiva sin una justificación o feedback previo del usuario.
- **Placeholders**: Dejar secciones vacías con comentarios como "TODO" o "TBD" en los archivos de documentación o especificaciones. Todo debe estar completamente desarrollado.
- **Actualizar sin Aprobación**: Modificar archivos de directrices centrales durante la codificación activa sin haber corrido el workflow de aprobación del plan.
