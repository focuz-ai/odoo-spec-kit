# Estándares de Desarrollo Frontend en Odoo (Frontend Standards)

## Tabla de Contenidos

1. [Stack Tecnológico](#stack-tecnológico)
2. [Estructura y Ciclo de Vida de Componentes OWL 2](#estructura-y-ciclo-de-vida-de-componentes-owl-2)
3. [Plantillas QWeb del Lado del Cliente](#plantillas-qweb-del-lado-del-cliente)
4. [Uso e Integración de Servicios del Core](#uso-e-integración-de-servicios-del-core)
5. [Registro de Assets en el Manifest](#registro-de-assets-en-el-manifest)
6. [Estilos SCSS y Diseño Responsivo](#estilos-scss-y-diseño-responsivo)
7. [Pruebas Frontend con QUnit y Web Test Helpers](#pruebas-frontend-con-qunit-y-web-test-helpers)
8. [Creación de Widgets de Campos Personalizados](#creación-de-widgets-de-campos-personalizados)
9. [Convenciones de Nombres y Estructura de Archivos](#convenciones-de-nombres-y-estructura-de-archivos)

---

## 1. Stack Tecnológico

El frontend del cliente web de Odoo está construido sobre las siguientes tecnologías principales:

- **OWL 2 (Odoo Web Library)**: Framework moderno de componentes reactivos basado en clases y hooks de JavaScript,
  adaptado al DOM virtual.
- **QWeb (XML)**: Motor de plantillas XML utilizado tanto para renderizado en servidor como para renderizado dinámico en
  cliente (JS).
- **Bootstrap 5**: Framework CSS subyacente personalizado para la estructura y componentes UI nativos.
- **SCSS**: Preprocesador de CSS utilizado para extender y modificar el diseño visual de Odoo.
- **QUnit**: El framework de pruebas unitarias y de integración oficial de Odoo para JavaScript.

---

## 2. Estructura y Ciclo de Vida de Componentes OWL 2

Todos los componentes de OWL 2 se definen utilizando clases estándar de ES6 que heredan de `Component` de `@odoo/owl`.

### Estructura Base de un Componente:

```javascript
import {Component, useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class MyComponent extends Component {
  static template = "my_module.MyComponent";
  static props = {
    message: {type: String, optional: true},
    active: Boolean,
    onChange: Function,
  };
  static defaultProps = {
    message: "Hello World",
  };

  setup() {
    // Reactive state initialization
    this.state = useState({
      counter: 0,
      loading: false,
    });

    // Core service injection
    this.notification = useService("notification");

    // Lifecycle hooks
    onWillStart(async () => {
      this.state.loading = true;
      await this._loadInitialData();
      this.state.loading = false;
    });

    onMounted(() => {
      console.log("Component mounted in the DOM");
    });

    onWillUnmount(() => {
      console.log("Component ready to be destroyed");
    });
  }

  async _loadInitialData() {
    // Simulation or server call
  }

  increment() {
    this.state.counter++;
    this.props.onChange(this.state.counter);
    this.notification.add(`Counter incremented to ${this.state.counter}`, {
      type: "info",
    });
  }
}
```

### Reglas Clave:

- **`setup()`**: Es el único punto de entrada para registrar hooks, inicializar el estado reactivo (`useState`) y
  consumir servicios (`useService`). No debe usarse el constructor clásico de ES6.
- **Props de Entrada**: Validar siempre las propiedades del componente declarando `static props`. Use tipos precisos y
  marque propiedades opcionales explícitamente.

---

## 3. Plantillas QWeb del Lado del Cliente

Las vistas frontend se definen mediante plantillas XML de QWeb. Se procesan de manera reactiva ante los cambios del
estado del componente.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<templates xml:space="preserve">
    <t t-name="my_module.MyComponent">
    <div class="o_my_module_component p-3 border rounded shadow-sm">
      <h4 class="mb-2">
        <t t-esc="props.message" />
      </h4>

      <p t-if="state.loading" class="text-muted">
                <i class="fa fa-spin fa-spinner me-1" />Loading data...
            </p>

      <t t-else="">
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-primary fs-6">
            <t t-esc="state.counter" />
          </span>
          <button
            class="btn btn-sm btn-outline-primary"
            t-on-click="increment"
            t-att-disabled="props.active ? '' : '1'"
          >
                        Increment
                    </button>
        </div>
      </t>

      <!-- Optional child content rendering via Slots -->
      <div class="mt-3 border-top pt-2" t-if="slots and slots.default">
        <t t-slot="default" />
      </div>
    </div>
  </t>
</templates>
```

### Directivas Esenciales:

- **`t-esc` / `t-out`**: Para evaluar y escapar/renderizar variables de texto en el DOM (en Odoo 16+, `t-out` reemplaza
  en la mayoría de los casos a `t-raw` por seguridad contra inyección XSS).
- **`t-if` / `t-elif` / `t-else`**: Para renderizado condicional.
- **`t-foreach` + `t-as`**: Para bucles iterativos. Es obligatorio incluir un atributo `t-key` único en el nodo hijo
  para optimizar el reconciliador del DOM virtual de OWL.
- **`t-att-*`**: Enlace dinámico de atributos (ej. `t-att-class`, `t-att-disabled`).
- **`t-on-*`**: Suscripción reactiva a eventos del navegador o de OWL (ej. `t-on-click`, `t-on-change`).

---

## 4. Uso e Integración de Servicios del Core

Odoo expone una arquitectura basada en servicios del core mediante el hook `useService("nombre_servicio")` dentro de
`setup()`.

### Servicios más Utilizados:

| Servicio           | Propósito                                                  | Ejemplo de Uso                                                              |
| ------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| **`orm`**          | Realizar consultas CRUD rápidas a modelos de base de datos | `this.orm.searchRead("res.partner", [["is_company", "=", true]], ["name"])` |
| **`rpc`**          | Llamar a métodos de Python customizados del backend        | `this.rpc("/my_module/my_json_route", { params })`                          |
| **`notification`** | Mostrar toasts informativos de éxito, alerta o peligro     | `this.notification.add("Success", { type: "success" })`                     |
| **`dialog`**       | Renderizar ventanas modales flotantes                      | `this.dialog.add(ConfirmationDialog, { body: "Confirm action" })`           |
| **`action`**       | Desparar acciones de ventana (`ir.actions.act_window`)     | `this.action.doAction("account.action_move_out_invoice_type")`              |
| **`user`**         | Obtener metadatos y contexto del usuario activo            | `const isCompanyUser = this.user.hasGroup("base.group_user")`               |

```javascript
// Example of an ORM query from a component
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

Odoo empaqueta todos los recursos de frontend (JS, CSS, SCSS, plantillas XML de QWeb) utilizando "Bundles" definidos en
el archivo `__manifest__.py`.

```python
# __manifest__.py
{
    'name': 'My Frontend Module',
    'version': '<ODOO_VERSION>.1.0.0',
    'depends': ['web'],
    'data': [
        # Traditional backend XML files go here (views, security)
    ],
    'assets': {
        # Main web client backend bundle (includes JS, XML, and SCSS)
        'web.assets_backend': [
            'my_module/static/src/js/**/*.js',
            'my_module/static/src/xml/**/*.xml',
            'my_module/static/src/scss/**/*.scss',
        ],
        # Unit/integration test bundle
        'web.assets_tests': [
            'my_module/static/tests/tours/**/*.js',
        ],
    },
}
```

> [!IMPORTANT] > **Registro en Odoo**: En Odoo+, las plantillas QWeb JS se registran directamente dentro del bundle
> principal (como `'web.assets_backend'`) y no bajo un bundle separado de QWeb. Además, todo recurso estático debe ser
> registrado en los assets del manifiesto y no importado mediante etiquetas de script/style en vistas XML.

---

## 6. Estilos SCSS y Diseño Responsivo

- **Espacio de Nombres Obligatorio**: Encapsule todos los estilos del módulo envolviéndolos en la clase contenedora de
  su componente utilizando el prefijo `.o_<modulo>_<nombre>` para evitar romper el diseño global del cliente web.
- **Variables de Odoo**: Reutilice las variables SCSS del backend de Odoo para colores de marca, márgenes y tipografías:
  - `$o-brand-odoo`: Color púrpura oficial de Odoo.
  - `$o-brand-primary`: Color primario activo.
  - `$o-view-background-color`: Fondo de la vista activa.
- **Evite `!important`**: El uso de `!important` debe evitarse siempre. Para sobreescribir estilos del core, incremente
  la especificidad CSS usando selectores más concretos.

```scss
// static/src/scss/my_component.scss
.o_my_module_component {
  background-color: $o-view-background-color;
  border: 1px solid rgba($o-brand-primary, 0.2);

  .o_counter_value {
    font-family: $o-font-family-monospace;
    color: $o-brand-odoo;
    font-size: 1.5rem;
  }
}
```

---

## 7. Pruebas Frontend con QUnit y Web Test Helpers

Odoo utiliza **QUnit** como su motor de pruebas unitarias y de integración oficial para JavaScript en el cliente web.

> [!IMPORTANT] **Prohibición de Herramientas E2E Externas**: Al igual que en el backend, queda terminantemente prohibido
> configurar o recomendar herramientas E2E de terceros (Playwright, Cypress, Selenium). El ecosistema de Odoo dicta que
> las pruebas de componentes puros se hacen con **QUnit**, y las simulaciones de flujo de usuario completo se hacen con
> **Odoo JS Tours**. No contamine el proyecto con dependencias E2E ajenas a Odoo.

### Conceptos Clave de QUnit:

- **`QUnit.module` / `QUnit.test`**: Para estructurar, agrupar y nombrar los casos de prueba.
- **`assert`**: Objeto que provee las aserciones de prueba (ej. `assert.strictEqual`, `assert.containsOnce`,
  `assert.ok`).
- **Helpers de Simulación**:
  - `makeTestEnv`: Inicializar un entorno de pruebas simulado del cliente web (`mock_env`).
  - `getFixture`: Obtener el contenedor DOM limpio de la suite para poder renderizar nuestro componente.
  - `mount`: Montar de forma asíncrona un componente OWL dentro de nuestro contenedor DOM de pruebas.
  - `nextTick`: Esperar de forma asíncrona al siguiente ciclo de renderizado del DOM de OWL después de cambiar el estado
    reactivo.
  - `click`: Helper para disparar un evento de click simulado sobre un selector DOM.
  - `patchWithCleanup`: Modificar temporalmente comportamientos de servicios o clases del core y restablecerlos
    automáticamente tras finalizar la prueba.

### Ejemplo de Test Unitario OWL con QUnit:

```javascript
// static/tests/my_component_tests.js
import {makeTestEnv} from "@web/../tests/helpers/mock_env";
import {getFixture, mount, nextTick, click} from "@web/../tests/helpers/utils";
import {MyComponent} from "../src/js/my_component";

let target;

QUnit.module("MyComponent OWL Tests", {
  beforeEach() {
    target = getFixture();
  },
});

QUnit.test("Should render the message and react to click", async (assert) => {
  let counterChanged = 0;

  const env = await makeTestEnv();
  await mount(MyComponent, target, {
    env,
    props: {
      message: "Unit Test",
      active: true,
      onChange: (val) => {
        counterChanged = val;
      },
    },
  });

  // Verify initial DOM rendering
  assert.containsOnce(target, ".o_my_module_component");
  assert.strictEqual(target.querySelector(".o_my_module_component h4").textContent.trim(), "Unit Test");
  assert.strictEqual(target.querySelector(".badge").textContent.trim(), "0");

  // Simulate a click on the increment button using the click helper
  await click(target, ".o_my_module_component button");
  await nextTick();

  // Verify state change and prop callback invocation
  assert.strictEqual(target.querySelector(".badge").textContent.trim(), "1");
  assert.strictEqual(counterChanged, 1);
});
```

---

## 8. Creación de Widgets de Campos Personalizados

En Odoo, los widgets de campos del formulario se crean extendiendo de `Component` de OWL 2, recibiendo propiedades
estándar del formulario en `props` (como `value` para el valor del campo y `update` para actualizarlo) y registrando la
clase directamente en el registry `fields`.

```javascript
// static/src/js/fields/my_color_field.js
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {Component} from "@odoo/owl";

export class MyColorField extends Component {
  get colorClass() {
    return `bg-${this.props.value || "light"}`;
  }

  selectColor(color) {
    // Update the field value by calling the update function provided in props
    this.props.update(color);
  }
}

MyColorField.template = "my_module.MyColorField";
MyColorField.props = {
  ...standardFieldProps,
};
MyColorField.supportedTypes = ["char", "selection"];

// Register the widget to make it usable in XML via widget="my_color_field"
registry.category("fields").add("my_color_field", MyColorField);
```

---

## 9. Convenciones de Nombres y Estructura de Archivos

- **JavaScript**: Utilice clases en `PascalCase` para componentes y nombres en `camelCase` para variables o servicios de
  negocio.
- **Archivos Estáticos**:
  - Un componente compuesto de JS + XML + SCSS debe compartir el mismo nombre base en minúsculas y snake_case (ej.
    `my_card.js`, `my_card.xml`, `my_card.scss`).
  - Guarde siempre los widgets en `static/src/js/fields/` o `static/src/components/`.
- **Plantillas QWeb**: El `t-name` de la plantilla XML debe coincidir exactamente con el nombre de clase completo
  calificado (ej. `my_module.MyComponent`).
