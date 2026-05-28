---
name: odoo-build-and-qa
description: Construye el código, verifica, realiza auditoría de seguridad y auto-repara en un bucle autónomo.
author: Focuz.io
version: 1.0.0
---

# Skill odoo-build-and-qa

Úsalo cuando el Spec técnico haya sido aprobado y el desarrollo deba ser implementado, auditado y estabilizado
autónomamente.

## Instrucciones

Eres un Orquestador Técnico. Para el ticket o feature proporcionado en `$ARGUMENTS`, debes ejecutar la siguiente cadena
de responsabilidades sin pedir intervención humana a menos que se agoten los intentos o se requiera una decisión de
negocio insalvable:

1. **Construcción (Apply):**
   - Utiliza rigurosamente la skill nativa `/openspec-apply-change` de OpenSpec para implementar todos los artefactos
     detallados en el Spec de manera estructurada.

2. **Verificación de la Implementación (Verify):**
   - Ejecuta rigurosamente la skill nativa `/openspec-verify-change` para validar que el código implementado empareje
     perfectamente con los artefactos de diseño y las especificaciones.
   - Corrige cualquier desviación antes de pasar a la auditoría técnica.

3. **Auditoría Base de Seguridad (Security Audit):**
   - Una vez verificado el código frente a la especificación, no consideres la tarea terminada.
   - Ejecuta e invoca tu skill `/odoo-security-audit` para auditar proactivamente la seguridad (ACLs, ir.rule,
     inyecciones SQL, XSS en QWeb).

4. **Revisión Adversarial (Red Team):**
   - **Obligatoriamente**, invoca y transfiere el control a tu skill `odoo-adversarial-review`.
   - Proporciónale los hallazgos de seguridad y auditoría previa.
   - Delega en esa skill la responsabilidad total de auditar a fondo la funcionalidad, el rendimiento y cumplimiento de directrices de Odoo frente a la Especificación Técnica.
   - **IMPORTANTE:** La skill de revisión adversarial NO repara código, solo emite un reporte de hallazgos y un veredicto (PASS/FAIL).

5. **Condiciones de Salida y Bucle de Reparación:**
   - Si la revisión adversarial arroja un **FAIL**, asume el control nuevamente. Deberás analizar el reporte de hallazgos e intentar realizar las correcciones necesarias en el código (Autoreparación) o detenerte y pedir ayuda al humano si el fallo es crítico o arquitectónico.
   - Si la revisión adversarial arroja **PASS** (código íntegro, seguro y óptimo), da por concluido el flujo y notifica que el módulo está listo para enviarse (`/odoo-ship`).
