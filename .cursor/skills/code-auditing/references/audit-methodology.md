# Metodología de Auditoría de Código (Odoo 16.0)

Guía operativa para ejecutar auditorías técnicas de addons Odoo 16.0 con foco en seguridad, comportamiento y
mantenibilidad.

## 1. Preparación

1. Definir alcance:
   - Addons y carpetas objetivo.
   - Tipo de auditoría (rápida, completa, pre-release, post-incidente).
2. Cargar contexto del proyecto:
   - `docs/base-standards.md`
   - `docs/backend-standards.md`
   - `docs/frontend-standards.md`
   - `docs/coding-guidelines.md`
3. Inventariar estructura del addon:
   - `__manifest__.py`, `__init__.py`
   - `models/`, `views/`, `security/`, `data/`, `report/`, `wizard(s)/`, `controllers/`, `static/`, `tests/`.
4. Tomar baseline:
   - Ejecutar validaciones automáticas disponibles (por ejemplo: `pre-commit run -a`).
   - Registrar warning/error inicial para diferenciar deuda existente vs deuda nueva.

## 2. Descubrimiento técnico

### 2.1 Backend y ORM

- Enumerar modelos `models.Model`, `models.TransientModel`, `models.AbstractModel`.
- Revisar herencias (`_inherit`, `_inherits`) y posibles conflictos.
- Identificar métodos críticos: `create`, `write`, `unlink`, cómputos, constraints, acciones.

### 2.2 Seguridad

- Mapear cada modelo contra `security/ir.model.access.csv`.
- Revisar record rules por grupo y dominio (`domain_force`).
- Auditar uso de `sudo()` y escalaciones de privilegio.
- Verificar SQL parametrizada en `self.env.cr.execute(...)`.

### 2.3 XML / Datos

- Validar consistencia de XML IDs, referencias y secuencia de carga del manifest.
- Revisar robustez de `xpath` y uso correcto de `attrs`/`states` en Odoo 16.
- Verificar botones/acciones expuestas sin grupo o control de estado.

### 2.4 Frontend OWL/QWeb

- Revisar componentes y hooks (`setup`, `onWillStart`, `onMounted`, etc.).
- Verificar consumo seguro de servicios (`orm`, `rpc`, `notification`, etc.).
- Auditar plantillas QWeb para evitar renderizado inseguro.
- Confirmar assets declarados en bundles del manifest.

### 2.5 Testing

- Revisar `tests/` y cobertura de casos críticos.
- Verificar uso de clases adecuadas (`TransactionCase`, `HttpCase`, QUnit según aplique).
- Señalar ausencia de pruebas para áreas de alto riesgo.

## 3. Análisis de hallazgos

Para cada hallazgo, documentar:

- Evidencia exacta (`archivo:línea`).
- Condición observada (hecho verificable).
- Riesgo técnico y operativo.
- Recomendación concreta alineada al estándar del repo.
- Estimación de esfuerzo (S/M/L/XL).

## 4. Patrones recurrentes

Buscar y consolidar problemas transversales:

- Deficiencias de seguridad repetidas (ACL, rules, `sudo`, SQL).
- Patrones de rendimiento ineficientes (N+1, loops no vectorizados, búsquedas redundantes).
- Inconsistencias de convención o arquitectura.
- Oportunidades de refactor para extensibilidad.

## 5. Priorización

Usar esta clasificación:

- **Critical**: Compromete seguridad, integridad de datos o disponibilidad.
- **High**: Riesgo alto de fallos funcionales o deuda severa.
- **Medium**: Problemas importantes pero no críticos.
- **Low**: Mejoras de consistencia o limpieza.
- **Quick Win**: Bajo esfuerzo y beneficio inmediato.

## 6. Formato de reporte

Orden recomendado:

1. Resumen ejecutivo (2-3 párrafos).
2. Hallazgos `Critical` y `High` (primero).
3. Hallazgos `Medium` y `Low`.
4. Quick wins.
5. Plan de remediación por etapas.
6. Riesgos residuales y supuestos.

Plantilla por issue:

```markdown
### [SEVERITY] Título

**Ubicación:** `addon/models/archivo.py:88`

**Problema:** Descripción verificable del problema.

**Impacto:** Riesgo técnico/negocio.

**Recomendación:** Cambio concreto propuesto.

**Esfuerzo:** S | M | L | XL
```

## 7. Verificaciones mínimas sugeridas

- `pre-commit run -a`
- Pruebas del módulo afectado (si el entorno Odoo está disponible).
- Revisión estática cruzada de modelos vs ACL.

Si no se pueden ejecutar pruebas por entorno, dejar constancia explícita en el reporte.

## 8. Errores comunes a evitar

1. Reportar hallazgos sin evidencia de línea.
2. Mezclar opiniones con hechos sin etiquetar supuestos.
3. Ignorar el impacto funcional al proponer refactors.
4. Evaluar seguridad solo en Python y omitir XML/controladores.
5. No diferenciar deuda preexistente de deuda introducida.
