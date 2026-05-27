# Estándares de Desarrollo Frontend en Odoo 19.0 (Frontend Standards)

## Tabla de Contenidos

1. [Stack Tecnológico](#stack-tecnológico)
2. [Estructura y Ciclo de Vida de Componentes OWL 2](#estructura-y-ciclo-de-vida-de-componentes-owl-2)
3. [Plantillas QWeb del Lado del Cliente](#plantillas-qweb-del-lado-del-cliente)
4. [Uso e Integración de Servicios del Core](#uso-e-integración-de-servicios-del-core)
5. [Registro de Assets en el Manifest](#registro-de-assets-en-el-manifest)
6. [Estilos SCSS y Diseño Responsivo](#estilos-scss-y-diseño-responsivo)
7. [Pruebas Frontend con HOOT y Web Test Helpers](#pruebas-frontend-con-hoot-y-web-test-helpers)
8. [Creación de Widgets de Campos Personalizados](#creación-de-widgets-de-campos-personalizados)
9. [Convenciones de Nombres y Estructura de Archivos](#convenciones-de-nombres-y-estructura-de-archivos)

---

## 1. Stack Tecnológico

El frontend del cliente web de Odoo 19.0 está construido sobre las siguientes
tecnologías principales:

- **OWL 2 (Odoo Web Library)**: Framework moderno de componentes reactivos basado en
  clases y hooks de JavaScript, adaptado al nuevo DOM virtual rápido (blockdom).
- **QWeb (XML)**: Motor de plantillas XML utilizado tanto para renderizado en servidor
  como para renderizado dinámico en cliente (JS).
- **Bootstrap 5**: Framework CSS subyacente personalizado para la estructura y
  componentes UI nativos.
- **SCSS**: Preprocesador de CSS utilizado para extender y modificar el diseño visual de
  Odoo.
- **HOOT**: El framework de pruebas unitarias y de integración oficial de Odoo para
  JavaScript.

---

## 2. Estructura y Ciclo de Vida de Componentes OWL 2

Todos los componentes de OWL 2 se definen utilizando clases estándar de ES6 que heredan
de `Component` de `@odoo/owl`.

### Estructura Base de un Componente:

```javascript
import {Component, useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class MiComponente extends Component {
  static template = "mi_modulo.MiComponente";
  static props = {
    mensaje: {type: String, optional: true},
    activo: Boolean,
    onCambio: Function,
  };
  static defaultProps = {
    mensaje: "Hola Mundo",
  };

  setup() {
    // Inicialización de estado reactivo
    this.state = useState({
      contador: 0,
      cargando: false,
    });

    // Inyección de servicios del core
    this.notification = useService("notification");

    // Ganchos del ciclo de vida (Hooks)
    onWillStart(async () => {
      this.state.cargando = true;
      await this._cargarDatosIniciales();
      this.state.cargando = false;
    });

    onMounted(() => {
      console.log("Componente montado en el DOM");
    });

    onWillUnmount(() => {
      console.log("Componente listo para ser destruido");
    });
  }

  async _cargarDatosIniciales() {
    // Simulación o llamada al servidor
  }

  incrementar() {
    this.state.contador++;
    this.props.onCambio(this.state.contador);
    this.notification.add(`Contador incrementado a ${this.state.contador}`, {
      type: "info",
    });
  }
}
```

### Reglas Clave:

- **`setup()`**: Es el único punto de entrada para registrar hooks, inicializar el
  estado reactivo (`useState`) y consumir servicios (`useService`). No debe usarse el
  constructor clásico de ES6.
- **Props de Entrada**: Validar siempre las propiedades del componente declarando
  `static props`. Use tipos precisos y marque propiedades opcionales explícitamente.

---

## 3. Plantillas QWeb del Lado del Cliente

Las vistas frontend se definen mediante plantillas XML de QWeb. Se procesan de manera
reactiva ante los cambios del estado del componente.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<templates xml:space="preserve">
    <t t-name="mi_modulo.MiComponente">
    <div class="o_mi_modulo_componente p-3 border rounded shadow-sm">
      <h4 class="mb-2">
        <t t-esc="props.mensaje" />
      </h4>

      <p t-if="state.cargando" class="text-muted">
                <i class="fa fa-spin fa-spinner me-1" />Cargando datos...
            </p>

      <t t-else="">
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-primary fs-6">
            <t t-esc="state.contador" />
          </span>
          <button
            class="btn btn-sm btn-outline-primary"
            t-on-click="incrementar"
            t-att-disabled="props.activo ? '' : '1'"
          >
                        Incrementar
                    </button>
        </div>
      </t>

      <!-- Renderizado de contenido hijo opcional a través de Slots -->
      <div class="mt-3 border-top pt-2" t-if="slots and slots.default">
        <t t-slot="default" />
      </div>
    </div>
  </t>
</templates>
```

### Directivas Esenciales:

- **`t-esc` / `t-out`**: Para evaluar y escapar/renderizar variables de texto en el DOM
  (en Odoo 18, `t-out` reemplaza en la mayoría de los casos a `t-raw` por seguridad
  contra inyección XSS).
- **`t-if` / `t-elif` / `t-else`**: Para renderizado condicional.
- **`t-foreach` + `t-as`**: Para bucles iterativos. Es obligatorio incluir un atributo
  `t-key` único en el nodo hijo para optimizar el reconciliador del DOM virtual de OWL.
- **`t-att-*`**: Enlace dinámico de atributos (ej. `t-att-class`, `t-att-disabled`).
- **`t-on-*`**: Suscripción reactiva a eventos del navegador o de OWL (ej. `t-on-click`,
  `t-on-change`).

---

## 4. Uso e Integración de Servicios del Core

Odoo expone una arquitectura basada en servicios del core mediante el hook
`useService("nombre_servicio")` dentro de `setup()`.

### Servicios más Utilizados:

| Servicio           | Propósito                                                  | Ejemplo de Uso                                                              |
| ------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| **`orm`**          | Realizar consultas CRUD rápidas a modelos de base de datos | `this.orm.searchRead("res.partner", [["is_company", "=", true]], ["name"])` |
| **`rpc`**          | Llamar a métodos de Python customizados del backend        | `this.rpc("/mi_modulo/mi_ruta_json", { params })`                           |
| **`notification`** | Mostrar toasts informativos de éxito, alerta o peligro     | `this.notification.add("Éxito", { type: "success" })`                       |
| **`dialog`**       | Renderizar ventanas modales flotantes                      | `this.dialog.add(ConfirmationDialog, { body: "Confirmar acción" })`         |
| **`action`**       | Desparar acciones de ventana (`ir.actions.act_window`)     | `this.action.doAction("account.action_move_out_invoice_type")`              |
| **`user`**         | Obtener metadatos y contexto del usuario activo            | `const isCompanyUser = this.user.hasGroup("base.group_user")`               |

```javascript
// Ejemplo de consulta ORM desde un componente
setup() {
    this.orm = useService("orm");
    onWillStart(async () => {
        this.partners = await this.orm.searchRead(
            "res.partner",
            [["is_company", "=", true]],
            ["name", "email"]
        );
    });
}
```

---

## 5. Registro de Assets en el Manifest

Odoo empaqueta todos los recursos de frontend (JS, CSS, SCSS, plantillas XML de QWeb)
utilizando "Bundles" definidos en el archivo `__manifest__.py`.

```python
# __manifest__.py
{
    'name': 'Mi Módulo Frontend',
    'version': '1.0',
    'depends': ['web'],
    'data': [
        # Archivos XML de backend tradicionales van aquí (vistas, security)
    ],
    'assets': {
        # Bundle principal del backend del cliente web
        'web.assets_backend': [
            'mi_modulo/static/src/js/**/*.js',
            'mi_modulo/static/src/scss/**/*.scss',
        ],
        # Bundle de plantillas QWeb JS (obligatorio en Odoo 18.0)
        'web.assets_qweb': [
            'mi_modulo/static/src/xml/**/*.xml',
        ],
        # Bundle de pruebas unitarias/integración
        'web.assets_tests': [
            'mi_modulo/static/tests/tours/**/*.js',
        ],
    },
}
```

> [!IMPORTANT] **Cambio en Odoo 18.0**: No se deben importar archivos JavaScript o SCSS
> directamente en las vistas XML usando etiquetas HTML. Todo recurso estático del
> cliente web debe ser registrado y empaquetado a través de los bundles de assets del
> manifiesto.

---

## 6. Estilos SCSS y Diseño Responsivo

- **Espacio de Nombres Obligatorio**: Encapsule todos los estilos del módulo
  envolviéndolos en la clase contenedora de su componente utilizando el prefijo
  `.o_<modulo>_<nombre>` para evitar romper el diseño global del cliente web.
- **Variables de Odoo**: Reutilice las variables SCSS del backend de Odoo para colores
  de marca, márgenes y tipografías:
  - `$o-brand-odoo`: Color púrpura oficial de Odoo.
  - `$o-brand-primary`: Color primario activo.
  - `$o-view-background-color`: Fondo de la vista activa.
- **Evite `!important`**: El uso de `!important` debe evitarse siempre. Para
  sobreescribir estilos del core, incremente la especificidad CSS usando selectores más
  concretos.

```scss
// static/src/scss/mi_componente.scss
.o_mi_modulo_componente {
  background-color: $o-view-background-color;
  border: 1px solid rgba($o-brand-primary, 0.2);

  .o_contador_valor {
    font-family: $o-font-family-monospace;
    color: $o-brand-odoo;
    font-size: 1.5rem;
  }
}
```

---

## 7. Pruebas Frontend con HOOT y Web Test Helpers

Odoo 18.0 introduce **HOOT**, un framework de pruebas moderno, rápido y modular.
Sustituye las pruebas basadas en QUnit e integra helpers avanzados de prueba en
`@web/../tests/web_test_helpers`.

### Conceptos Clave de HOOT:

- **`describe` / `test`**: Para estructurar y modularizar los casos de prueba.
- **`expect`**: Aseveraciones con sintaxis fluida.
- **Helpers de Simulación**:
  - `defineModels`: Cargar y simular la existencia de modelos ORM virtuales o del núcleo
    para la prueba.
  - `mountView`: Montar una vista declarativa XML ficticia o real.
  - `onRpc`: Simular y capturar llamadas RPC/ORM hacia el backend.
  - `patchWithCleanup`: Modificar temporalmente métodos o servicios y deshacer el parche
    automáticamente al finalizar el test.
  - `mountWithCleanup`: Montar un componente OWL limpiando el DOM virtual y listeners
    después de cada prueba.

### Ejemplo de Test Unitario OWL con HOOT:

```javascript
// static/tests/mi_componente_tests.js
import {describe, test, expect} from "@odoo/hoot";
import {mountWithCleanup} from "@web/../tests/web_test_helpers";
import {MiComponente} from "../src/js/mi_componente";

describe("MiComponente OWL Tests", () => {
  test("Debería renderizar el mensaje y reaccionar al click", async () => {
    let contadorCambio = 0;

    // Montar el componente con propiedades y simulación
    const comp = await mountWithCleanup(MiComponente, {
      props: {
        mensaje: "Test Unitario",
        activo: true,
        onCambio: (val) => {
          contadorCambio = val;
        },
      },
    });

    // Verificar el renderizado inicial en el DOM
    expect(".o_mi_modulo_componente").toExist();
    expect(".o_mi_modulo_componente h4").toHaveText("Test Unitario");
    expect(".badge").toHaveText("0");

    // Simular click en el botón de incrementar usando HOOT-dom helpers
    await click(".o_mi_modulo_componente button");

    // Verificar cambio de estado y llamada al callback prop
    expect(".badge").toHaveText("1");
    expect(contadorCambio).toBe(1);
  });
});
```

---

## 8. Creación de Widgets de Campos Personalizados

En Odoo 19.0, los widgets de campos del formulario se crean heredando del componente
base y registrándolos en el `fields` registry. Es altamente recomendado el uso del hook
`useRecordObserver` para reaccionar ante cambios en los datos del recordset de forma
limpia:

```javascript
// static/src/js/campos/mi_campo_color.js
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useRecordObserver} from "@web/model/relational_model/utils";
import {Component, useState} from "@odoo/owl";

export class MiCampoColor extends Component {
  static template = "mi_modulo.MiCampoColor";
  static props = {
    ...standardFieldProps,
  };

  setup() {
    this.state = useState({
      valorColor: "light",
    });

    // Escuchar cambios reactivos en el registro (Recomendado en Odoo 19.0)
    useRecordObserver((record) => {
      this.state.valorColor = record.data[this.props.name] || "light";
    });
  }

  get colorClass() {
    return `bg-${this.state.valorColor}`;
  }

  seleccionarColor(color) {
    // Actualizar el valor del campo en el recordset del formulario
    this.props.record.update({[this.props.name]: color});
  }
}

// Registrar el widget para hacerlo utilizable en XML mediante widget="mi_campo_color"
registry.category("fields").add("mi_campo_color", {
  component: MiCampoColor,
  supportedTypes: ["char", "selection"],
});
```

---

## 9. Convenciones de Nombres y Estructura de Archivos

- **JavaScript**: Utilice clases en `PascalCase` para componentes y nombres en
  `camelCase` para variables o servicios de negocio.
- **Archivos Estáticos**:
  - Un componente compuesto de JS + XML + SCSS debe compartir el mismo nombre base en
    minúsculas y snake_case (ej. `mi_tarjeta.js`, `mi_tarjeta.xml`, `mi_tarjeta.scss`).
  - Guarde siempre los widgets en `static/src/js/fields/` o `static/src/components/`.
- **Plantillas QWeb**: El `t-name` de la plantilla XML debe coincidir exactamente con el
  nombre de clase completo calificado (ej. `mi_modulo.MiComponente`).
