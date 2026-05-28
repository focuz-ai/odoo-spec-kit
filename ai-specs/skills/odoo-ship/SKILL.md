---
name: odoo-ship
description:
  Orquestador final que archiva el ticket completado y realiza el commit estructurado siguiendo los estándares de Odoo.
author: Focuz.io
version: 1.0.0
---

# Skill odoo-ship

Úsalo cuando el desarrollo del ticket ha finalizado, fue testeado, auditado y está listo para integrarse definitivamente
al código base.

## Instrucciones

Eres el Release Manager. Para el ticket proporcionado en `$ARGUMENTS`, debes orquestar el proceso de cierre y versionado
del código en un flujo ininterrumpido.

Sigue estos pasos en orden secuencial:

1. **Sincronización (Sync Specs):**
   - Antes de archivar, utiliza obligatoriamente la skill nativa `/openspec-sync-specs` de OpenSpec para sincronizar y
     actualizar las especificaciones principales (main specs) con los cambios implementados en el delta spec actual.

2. **Archivado (Archive):**
   - Ejecuta las instrucciones de la skill nativa `/openspec-archive-change` de OpenSpec para trasladar y cerrar el
     ciclo del documento de Especificación (Spec) según los estándares del framework.
   - Si estás integrado con un sistema de tickets (Jira / Plane MCP), actualiza el estado del ticket a "Done",
     "Resolved" o "Ready for Merge".

3. **Versionado (Commit Odoo):**
   - Antes de crear el commit, es **obligatorio** que leas y proceses las instrucciones de la skill `/odoo-commit`.
   - Aplica rigurosamente las reglas definidas en dicha skill para estructurar los mensajes de commit en español, pero
     siguiendo los _Git Guidelines_ de Odoo (por ejemplo, `[IMP] module_name: mejora de la vista`).
   - Prepara el stage de los archivos correspondientes y efectúa el commit en el repositorio local.

4. **Cierre de Ciclo:**
   - Informa al usuario que el flujo ha concluido exitosamente.
   - Muestra en tu respuesta el mensaje de commit generado y confirma la ruta donde quedó archivado el Spec.
