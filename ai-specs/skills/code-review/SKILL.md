---
name: code-review
description:
  Ejecuta la revisión adversarial de código, cruce estático de seguridad y el bucle
  autónomo de autoreparación ante fallos de pruebas en Odoo 18.0.
author: Focuz AI
version: 1.0.0
---

# Skill: Revisión de Código y Bucle de Autoreparación (/code-review)

Esta skill consolida la auditoría de calidad y seguridad adversarial y maneja de forma
autónoma la corrección de errores de pruebas en Odoo 18.0.

---

## 1. Fase 1: Cruce de Seguridad Estático (ACLs)

Antes de cualquier análisis dinámico, el agente debe realizar la verificación estática
de permisos del módulo:

- **Escaneo de Modelos**: Buscar en los archivos de Python todas las declaraciones de
  modelos nuevos (`class ... (models.Model):` y `class ... (models.TransientModel):`).
- **Verificación en CSV**: Confirmar que cada uno de estos modelos posea exactamente una
  fila de permisos declarada en el archivo `security/ir.model.access.csv`.
- **Acción**: Si falta alguna declaración de permisos, el agente debe considerarlo como
  un **Blocker** y resolverlo inmediatamente agregando la fila correspondiente al CSV
  para evitar warnings del arranque de Odoo.

---

## 2. Fase 2: Auditoría de Seguridad Adversarial

Realizar un escaneo del código desarrollado para detectar los siguientes riesgos
específicos de Odoo:

- **Inyección SQL**: Verificar que no existan queries crudas concatenadas. Validar que
  toda ejecución con `self.env.cr.execute()` utilice la composición segura mediante la
  clase `odoo.tools.SQL`.
- **Abuso de `sudo()`**: Rastrear todas las llamadas a `.sudo()`. Validar que estén
  plenamente justificadas y que no permitan accesos no autorizados indirectos
  (IDOR/Escalada de privilegios).
- **Validaciones de Entrada**: Confirmar que los métodos que procesen datos externos
  apliquen restricciones `@api.constrains` o lancen excepciones `UserError` /
  `ValidationError` nativas de Odoo ante datos inválidos.

---

## 3. Fase 3: Adherencia a Directrices

Confirmar la compatibilidad estricta del código con:

- `docs/coding-guidelines.md` (orden de atributos en modelos, nombres descriptivos,
  traducción con `%`).
- `docs/backend-standards.md` (multicompañía, uso de helpers `Command`).
- `docs/frontend-standards.md` (SCSS namespaces, reactividad de OWL, HOOT).

---

## 4. Bucle Autónomo de Autoreparación (Self-Repair Loop)

> [!IMPORTANT] **Bucle de Autoreparación Autónomo (Hasta 3 Intentos)**
>
> Si las pruebas ejecutadas previamente (por `/verify` o comandos locales) arrojaron
> fallos, o si las fases 1 y 2 de este review encontraron anomalías, el agente debe
> intentar autoreparar el código de forma autónoma siguiendo este flujo:

### Ciclo del Bucle (Máximo 3 ciclos):

1. **Analizar Contexto de Entrada Limpio**:
   - Extraer un **traceback limpio** (remover todo el boilerplate interno de imports y
     bootstrap de Odoo para enfocarse en la línea exacta del fallo en nuestro módulo).
   - Obtener el `git diff` de los últimos cambios aplicados.
2. **Restablecer Estado/Transacción**:
   - Dado que Odoo ejecuta sus tests de transacción bajo savepoints, antes de cada
     reintento de prueba asegúrese de revertir o limpiar la base de datos de pruebas si
     quedó en un estado corrupto.
3. **Aplicar la Corrección Quirúrgica**:
   - Modificar el código fuente de forma puntual para solucionar el fallo detectado.
4. **Re-ejecutar Verificación**:
   - Disparar de nuevo el test runner de Odoo (`/verify` o comando de test específico).
   - Si los tests pasan con éxito: Finalizar el bucle con un veredicto de **éxito**
     (`PASS`).
   - Si los tests vuelven a fallar: Incrementar el contador de intentos y repetir desde
     el paso 1.

### Límite de Intentos:

- Si tras **3 intentos** de autoreparación el error persiste, el agente debe detener el
  bucle y redactar un reporte detallado para el desarrollador humano (bloqueo),
  indicando las soluciones intentadas y el traceback limpio restante.

---

## 5. Formato de Veredicto

El veredicto final impreso por el agente en la consola debe estructurarse como:

```markdown
## Resultado del Code-Review

### 1. Cruce Estático de Seguridad

- [x] Modelos verificados en CSV: OK / Listar faltantes.

### 2. Hallazgos Adversariales

| Nivel                   | Componente | Descripción del Riesgo | Sugerencia |
| ----------------------- | ---------- | ---------------------- | ---------- |
| Blocker / Mayor / Minor |            |                        |            |

### 3. Historial del Bucle de Autoreparación

- **Intentos realizados**: X / 3
- **Traceback corregido**: `<snippet>`
- **Estado final**: Resuelto / Bloqueado

### Veredicto Final

**PASS** | **FAIL**
```
