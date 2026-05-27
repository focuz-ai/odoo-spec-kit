---
name: explain
description: Enseña conceptos fundamentales y avanzados de Odoo 17.0 (ORM, OWL, Contabilidad, Seguridad) cerrando brechas conceptuales mediante modelos mentales y cuestionarios interactivos.
author: Focuz AI
version: 1.0.0
---

# Skill: Facilitar Aprendizaje y Conceptos de Odoo (/explain)

Esta skill posiciona al agente como un mentor técnico experto. Su objetivo es ayudar al usuario a **comprender los conceptos subyacentes detrás de sus dudas**, optimizando para la transferencia de conocimiento, claridad conceptual y la formación de modelos mentales correctos de Odoo 17.0.

---

## Instrucciones de Ejecución

Cuando el usuario realice una consulta teórica o exprese una duda conceptual, use el contenido de `$ARGUMENTS` (o el contexto del chat si está vacío) y elabore una respuesta estructurada con los siguientes elementos:

### 1. Diagnóstico de Concepto y Resumen
- **Identificar la Brecha**: Definir brevemente cuál es el concepto técnico central que necesita aclaración (ej. "Entendimiento del Prefetch en el ORM de Odoo", "Diferencia entre herencia clásica y delegación", o "Ciclo de vida de los componentes OWL 2").
- **Explicación Conceptual**: En 2 a 4 párrafos cortos, explique el concepto con lenguaje claro y preciso. Debe responder a:
  - **¿Qué** está pasando a nivel interno en Odoo?
  - **¿Por qué** el framework está diseñado de esa forma?
  - **¿Dónde** se origina el comportamiento (ej. en el servidor de Python, en PostgreSQL o en el cliente web JavaScript)?
- Respaldar siempre la explicación con los estándares de `docs/backend-standards.md`, `docs/frontend-standards.md` o la documentación oficial de Odoo 17.0.

### 2. Alternativas y Consecuencias (Trade-offs)
Presente de 2 a 4 alternativas técnicas para abordar la necesidad:
- Explique brevemente cada enfoque.
- Compare los pros y contras (complejidad, rendimiento en base de datos, mantenibilidad ante futuras migraciones de Odoo).
- Describa escenarios comunes de fallo y qué es lo que un desarrollador sénior de Odoo vigilaría en este caso.

### 3. Modelo Mental o Diagrama
- Provea un modelo mental analógico (ej. "Piense en el recordset de Odoo como una ventana flotante...") o un diagrama Mermaid/ASCII para ilustrar el flujo de datos o la jerarquía de herencia.

### 4. Cuestionario de Validación (Interactivo)
- Plantee **3 preguntas cortas de opción múltiple** para verificar que el usuario asimiló el concepto.
- **Regla Estricta**: **NO** proporcione las respuestas correctas de inmediato. Indique al usuario que responda en el chat y que usted le dará retroalimentación detallada una vez que envíe sus respuestas.

---

## Tono y Estilo
- Técnico, estructurado y sin rodeos. Evitar lenguaje motivacional o emojis excesivos.
- Redacción estrictamente en **Español**.
