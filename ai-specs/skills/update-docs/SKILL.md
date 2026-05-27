---
name: update-docs
description:
  Identifica y actualiza la documentación técnica requerida tras realizar cambios en el
  código de Odoo, guiándose por los estándares de documentación del proyecto.
author: Focuz AI
version: 1.0.0
---

# Skill: Actualizar Documentación (/update-docs)

Esta skill indica al agente que debe escanear el conjunto de cambios realizados en el
módulo de Odoo y actualizar la documentación técnica correspondiente.

---

## Instrucciones de Ejecución

1. Analizar el alcance de los cambios aplicados en la rama git.
2. Cargar y seguir las directrices especificadas en `docs/documentation-standards.md`
   para identificar qué archivos requieren actualización.
3. Actualizar la documentación técnica (ej. `docs/data-model.md` para modelos/campos,
   `docs/api-spec.md` para controladores) redactando el contenido de forma clara y
   rigurosa en **Español**.
4. Informar al usuario en el chat sobre cuáles archivos de documentación fueron
   actualizados y el resumen de los cambios añadidos.
