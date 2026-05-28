---
name: security-audit
description:
  Realiza la auditoría estática de seguridad y permisos en módulos de Odoo EE 16.0.
  Cruza ACLs, reglas de registro, detecta inyecciones SQL y previene XSS en vistas QWeb.
author: Focuz.io
version: 1.0.0
---

# Skill: Auditoría de Seguridad (/security-audit)

Esta skill consolida la auditoría estricta de seguridad y permisos para Odoo 16.0 Enterprise Edition.
Debe ejecutarse para prevenir brechas de seguridad, fugas de datos entre compañías o escaladas de privilegios no autorizadas.

---

## 1. Fase 1: Cruce Estático de Seguridad (ACLs)

Verificación estática de permisos del modelo:

- **Escaneo de Modelos**: Buscar en los archivos de Python todas las declaraciones de modelos nuevos
  (`class ... (models.Model):` y `class ... (models.TransientModel):`).
- **Verificación en CSV**: Confirmar que cada uno de estos modelos posea exactamente una fila de permisos declarada en
  el archivo `security/ir.model.access.csv`.
- **Acción**: Si falta alguna declaración de permisos, el agente debe considerarlo como un **Blocker** e indicarlo en el reporte final.

---

## 2. Fase 2: Reglas de Registro Multi-compañía (ir.rule)

Validación de aislamiento de datos corporativos:

- **Detección de Campos Company**: Identificar si los modelos nuevos declaran el campo `company_id`.
- **Verificación de Reglas**: Si un modelo tiene `company_id`, se DEBE exigir la existencia de una regla de registro (`ir.rule`) en los archivos XML de seguridad que aísle los registros por compañía (ej. `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`).
- **Acción**: Marcar la ausencia de esta regla en modelos con `company_id` como un riesgo **Blocker**.

---

## 3. Fase 3: Seguridad en Vistas (QWeb)

Prevención de vulnerabilidades Cross-Site Scripting (XSS) en frontend/backend:

- **Escaneo de Directivas QWeb**: Inspeccionar todos los archivos XML en busca de la directiva `t-raw`.
- **Regla Estricta**: En Odoo 15+, el uso de `t-raw` es obsoleto y peligroso. Exigir su reemplazo por `t-out` (para HTML sanitizado de forma segura) o `t-esc` (para escape de texto plano).

---

## 4. Fase 4: Auditoría de Seguridad Adversarial (Backend)

Escaneo del código de Python para detectar riesgos críticos:

- **Inyección SQL**: Verificar que no existan queries crudas concatenadas con strings (ej. `f"SELECT * FROM {table}"`). Validar que toda ejecución con `self.env.cr.execute()` utilice paso de parámetros `%s` o la composición segura de la clase `odoo.tools.SQL`.
- **Abuso de `sudo()`**: Rastrear todas las llamadas a `.sudo()`. Validar que estén plenamente justificadas, limitadas al alcance mínimo necesario y que no permitan accesos no autorizados indirectos (ej. IDOR o escalada de privilegios basada en inputs del usuario).

---

## 5. Formato de Veredicto de Seguridad

Al finalizar, el agente debe imprimir el siguiente reporte en consola:

```markdown
## Resultado de Auditoría de Seguridad

### 1. Cruce Estático de Seguridad (ACLs)
- [x] Modelos verificados en CSV: OK / Listar faltantes.

### 2. Reglas de Registro Multi-compañía
- [x] Modelos con `company_id` asegurados: OK / N/A / Listar modelos sin ir.rule.

### 3. Hallazgos Adversariales y Frontend

| Nivel                   | Componente | Descripción del Riesgo | Sugerencia |
| ----------------------- | ---------- | ---------------------- | ---------- |
| Blocker / Mayor / Minor |            |                        |            |

### Veredicto Final de Seguridad
**PASS** | **FAIL**
```
