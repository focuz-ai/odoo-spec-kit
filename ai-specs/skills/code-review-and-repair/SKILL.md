---
name: code-review-and-repair
description:
  Revisa la funcionalidad, rendimiento y cumplimiento de directrices del código Odoo.
  Incluye verificación contra el Spec Funcional (SDD) y un bucle de autoreparación autónomo ante fallos.
author: Focuz.io
version: 1.0.0
---

# Skill: Code Review y Bucle de Autoreparación (/code-review-and-repair)

Esta skill consolida la auditoría de calidad funcional, rendimiento y el manejo autónomo de la corrección de errores en Odoo 16.0 Enterprise, basándose en la filosofía de Spec-Driven Development (SDD).

---

## 1. Fase 0: Trazabilidad del Spec (Spec-Driven Verification)

Antes de validar código, el agente debe alinear la implementación con los requerimientos originales:

- **Lectura del Spec Funcional**: Buscar y leer el archivo de especificación funcional en `ai-specs/features/`.
- **Cruce de Criterios de Aceptación (AC)**: Verificar que cada *Acceptance Criteria* tenga código que lo implemente y tests asociados.
- **Detección de Shadow IT**: Identificar modelos, campos o lógicas que no fueron solicitadas en la especificación y marcarlas como anomalías, recomendando su extracción o justificación.

---

## 2. Fase 1: Auditoría de Performance (Anti-Patrones ORM)

Odoo sufre severamente por consultas N+1 en Python. El agente debe:

- **Escaneo de Bucles**: Buscar operaciones ORM (`.search()`, `.write()`, `.create()`) o llamadas a `.mapped()` costosas DENTRO de bucles `for`.
- **Acción**: Marcar como un defecto y recomendar (o aplicar en la autoreparación) una refactorización para extraer el acceso a base de datos del bucle operando en modo batch (sobre conjuntos de registros enteros).

---

## 3. Fase 2: Adherencia a Directrices y Buenas Prácticas

Confirmar la compatibilidad estricta del código con:

- `docs/coding-guidelines.md` (orden de atributos, traducciones).
- `docs/backend-standards.md` (validaciones `@api.constrains`, excepciones nativas `UserError`, dependencias estrictas en `@api.depends`, y no permitir CRUD dentro de `@api.onchange`).
- `docs/frontend-standards.md` (namespaces SCSS, modularidad OWL).

---

## 4. Fase 3: Bucle Autónomo de Autoreparación (Self-Repair Loop)

> [!IMPORTANT]
> **Bucle de Autoreparación Autónomo (Hasta 3 Intentos)**
>
> Si las pruebas fallan o las fases previas encuentran defectos que rompen el pipeline, el agente intentará autoreparar el código:

### Ciclo del Bucle (Máximo 3 ciclos):

1. **Linter Fast-Fail (Pre-chequeo)**:
   - Antes de ejecutar tests pesados de Odoo, ejecutar validadores sintácticos locales (ej. `flake8` o herramientas similares configuradas) para fallar rápido en caso de errores de indentación o imports faltantes.
2. **Analizar Contexto (Traceback Limpio)**:
   - Si Odoo falla, extraer la parte relevante del error ignorando el bootstrap interno del framework.
3. **Root Cause Analysis (RCA)**:
   - *Obligatorio:* El agente debe declarar explícitamente en texto la causa raíz: *"La causa raíz del fallo en la línea X es Y. Se solucionará haciendo Z porque..."*.
4. **Restablecer Estado/Transacción**:
   - Revertir o limpiar la base de datos de pruebas si quedó en un estado corrupto (crucial en Odoo).
5. **Aplicar Corrección Quirúrgica**:
   - Modificar solo las líneas afectadas.
6. **Re-ejecutar Verificación**:
   - Disparar de nuevo el test runner de Odoo (`/verify`).
   - Si pasa: Emitir veredicto `PASS`.
   - Si falla: Repetir desde Paso 1 incrementando el contador.

### Límite de Intentos:
- Al alcanzar los **3 intentos** sin éxito, detener el bucle, bloquear y proveer el reporte RCA y los diffs aplicados al humano.

---

## 5. Formato de Veredicto

El veredicto final en la consola debe estructurarse como:

```markdown
## Resultado de Code-Review Funcional

### 1. Trazabilidad del Spec (SDD)
- [x] Cobertura de ACs: X/Y implementados.
- [x] Anomalías (Shadow IT): Ninguna / Detectadas.

### 2. Auditoría de Performance y Directrices
- [x] Anti-patrones N+1: Resueltos / Listar métodos problemáticos.
- [x] Apego a Directrices: OK / Desviaciones encontradas.

### 3. Historial del Bucle de Autoreparación
- **Intentos realizados**: X / 3
- **Último RCA**: `<snippet del razonamiento>`
- **Estado final**: Resuelto / Bloqueado

### Veredicto Final
**PASS** | **FAIL**
```
