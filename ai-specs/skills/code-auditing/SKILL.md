---
name: code-auditing
description:
  Metodología estructurada en español para realizar auditorías de calidad de código y detectar deuda técnica en módulos
  Odoo.
version: 2.0.0
---

# Skill: Code Auditing (Odoo)

Metodología integral para auditar calidad, seguridad, mantenibilidad y deuda técnica en código Odoo (backend,
vistas XML y frontend OWL/QWeb).

## Cuándo usar

- Auditorías técnicas completas de uno o más addons Odoo.
- Revisión previa a merge/release.
- Evaluación de deuda técnica y riesgos de seguridad.
- Verificación de cumplimiento de estándares del repo (`docs/*.md`).
- Seguimiento tras cambios grandes de arquitectura o refactors.

## Reglas de ejecución

1. Priorizar evidencia verificable sobre suposiciones.
2. Citar siempre archivo y línea para cada hallazgo.
3. Mantener foco en comportamiento, seguridad y riesgo operativo.
4. No proponer cambios que rompan compatibilidad sin indicarlo explícitamente.
5. Respetar estándares del proyecto:
   - `docs/base-standards.md`
   - `docs/backend-standards.md`
   - `docs/frontend-standards.md`
   - `docs/coding-guidelines.md`
   - `docs/git-guidelines.md`

## Fases de auditoría

### Fase 0: Contexto y baseline

1. Identificar alcance (addon/es, carpetas, versión Odoo, dependencias).
2. Revisar `__manifest__.py`, `README.md`, `security/`, `models/`, `views/`, `data/`, `static/`, `tests/`.
3. Ejecutar baseline local disponible (ej. `pre-commit run -a`) y registrar resultados.
4. Preparar checklist de validación para backend, seguridad, XML y OWL/QWeb.

### Fase 1: Descubrimiento estructural

1. Enumerar modelos persistentes, transitorios y abstractos.
2. Inventariar vistas (form, tree/list, search, kanban, qweb reports).
3. Inventariar controladores (`controllers/`) y wizards (`wizard/` o `wizards/`).
4. Inventariar assets frontend y tests.
5. Mapear ACLs y reglas de registro por modelo.

### Fase 2: Análisis técnico por categoría

Para cada archivo relevante, analizar:

- Seguridad:
  - ACL faltantes en `ir.model.access.csv`.
  - Record rules débiles o sobrepermisivas.
  - Uso inseguro de `sudo()`.
  - SQL sin parametrizar.
  - Exposición de datos sensibles en endpoints/controladores.
- ORM y consistencia de negocio:
  - `@api.model_create_multi` en `create`.
  - Correcto uso de `check_company=True` en relacionales multiempresa.
  - Riesgos N+1, uso ineficiente de recordsets, ausencia de `read_group` cuando aplica.
  - Uso de `Command` en x2many en lugar de tuplas crudas.
  - Ausencia de validaciones (`@api.constrains`, `@api.onchange`) cuando son críticas.
- Vistas XML y datos:
  - XPath frágiles o IDs inconsistentes.
  - `attrs`/`states` incorrectos para Odoo 16.
  - Acciones/botones sin control de permisos.
  - Inconsistencias entre datos XML y modelos destino.
- Frontend OWL/QWeb:
  - Uso correcto de `setup()`, hooks y servicios.
  - Riesgos de XSS por renderizado indebido.
  - Assets no registrados en `__manifest__.py`.
  - Falta de tests QUnit en cambios críticos de UI.
- Testing y mantenibilidad:
  - Cobertura insuficiente en `tests/` para lógica sensible.
  - Código duplicado, métodos monolíticos y deuda de diseño.
  - Convenciones de nombres/estructura fuera de guías del repo.

### Fase 3: Detección de patrones sistémicos

1. Hallar problemas repetidos entre archivos (seguridad, estilo, rendimiento).
2. Detectar acoplamientos innecesarios o extensibilidad limitada.
3. Proponer agrupación de refactors por impacto y riesgo.

### Fase 4: Priorización y plan de remediación

Clasificar hallazgos por severidad:

- Critical: fallo de seguridad o corrupción de datos.
- High: riesgo operativo, funcional o de mantenibilidad alta.
- Medium: incumplimiento técnico con impacto moderado.
- Low: mejora de calidad/consistencia.
- Quick Win: corrección de bajo esfuerzo y alto valor.

### Fase 5: Reporte final

Generar un reporte con:

1. Resumen ejecutivo.
2. Hallazgos por severidad (con `archivo:línea`).
3. Riesgo e impacto de negocio/técnico.
4. Recomendación concreta y esfuerzo estimado (S/M/L/XL).
5. Secuencia sugerida de implementación.

## Formato de hallazgo

```markdown
### [SEVERITY] Título breve

**Ubicación:** `ruta/archivo.py:123`

**Problema:** Descripción del riesgo observado.

**Impacto:** Efecto técnico o de negocio.

**Recomendación:** Cambio sugerido alineado a Odoo 16 y estándares del repo.

**Esfuerzo:** S | M | L | XL
```

## Checklist rápido

### Antes de auditar

- [ ] Definir alcance técnico y funcional.
- [ ] Revisar estándares `docs/*.md` del repo.
- [ ] Tomar baseline de validaciones automáticas.

### Durante auditoría

- [ ] Registrar evidencia con archivo y línea.
- [ ] Separar hechos verificados de inferencias.
- [ ] Priorizar hallazgos por riesgo real.

### Cierre

- [ ] Entregar reporte completo y accionable.
- [ ] Incluir quick wins y plan por etapas.
- [ ] Señalar riesgos residuales y cobertura faltante.

## Recursos

- `references/audit-methodology.md` - Metodología detallada de auditoría Odoo.
- `references/dead-code-methodology.md` - Metodología para detección segura de código muerto en Odoo.
