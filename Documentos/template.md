# Titulo: Prototipo De Una Aplicación Web Para El Almacenamiento De Información Sobre La Gestión De Residuos Electrónicos En La Localidad De Chapinero
---
## Overview: Problema a resolver
Descripción..

### Alcance(Scope)
Descripción..

#### Casos de uso
* Caso de uso 1 - Registrar Usuario
Descripción: Para el registro de un nuevo usuario el software solicitará al mismo la siguiente información: Nombre, Correo, Fecha de nacimiento, Número de teléfono y ocupación.
Una vez realizado el registro se enviará un correo de confirmación el cual le permitirá re dirigirse al menú principal de la aplicación. 

```plantuml

@startuml


Persona --> (Diligenciar Datos)
(Diligenciar Datos) -> (Validar Información) :include

@enduml
```

* Caso de uso 2 - Consultar reciclaje por usuario
Descripción: El usuario podrá visualizar la cantidad de puntos que posee, van a estar listados en una tabla con la fecha, lugar y cantidad de desechos electrónicos depositados, con una breve descripción del electrodoméstico. El administrador podrá ver esta descripción,  podrá eliminar o modificar los datos de la misma.
```plantuml
@startuml

Usuario --> (Consultar reciclaje almacenado ) 
Administrador --> (Consultar reciclaje almacenado) 
    
(Consultar reciclaje almacenado) -> (Listar Usuario) :include
(Consultar reciclaje almacenado) -> (Seleccionar Usuario) :include



@enduml
```
* Caso de uso 3 - Visualizar meta de reciclaje
Descripción: A cada usuario se le asignará una meta para poder reclamar su bonificación, por ejemplo: si el usuario quiere reclamar boletos para cine necesitará x cantidad de reciclaje. Esto se hace con el fin de incentivar al usuario a depositar sus electrodomésticos. Además, podrá ver su meta en semanas o en meses.

```plantuml
@startuml

Usuario --> (Visualizar Meta) 
    
(Visualizar Meta) -> (Meta Semanal) :extend
(Visualizar Meta) -> (Meta Mesual) :extend


@enduml
```
* Caso de uso 4 - Enviar mensaje al administrador.
Descipcion: El usuario podrá enviar y visualizar los mensajes, se presentarán varias opciones para modificar el texto adjuntado. Se tendrá un apartado para enviar archivos adjuntos y aparecerá una lista con los archivos adjuntos y el tipo de archivo.

```plantuml
@startuml
Usuario --> (Procesar publicacion de emnsaje)
(Procesar publicacion de emnsaje) -> (listar solicitudes pendientes) :extend
Administrado --> (listar solicitudes pendientes)
@enduml
```
* Caso de uso 5 - Consultar sitio de reciclaje.
Descripcion: El usuario podrá consultar su sitio de reciclaje más cercano, al ingresar le pedirá al usuario su ubicación y le permitirá ver el eco-punto más cercano.
```plantuml
@startuml
Usuario --> (sonsultar Sitio de Reciclaje)
@enduml
```
* Caso de uso 6 - Agregar Sponsor.
Descripcion: Un sponsor que no tiene que estar registrado en la aplicación, se podrá comunicar con un administrador para ofrecer sus servicios a los usuarios (Bonificaciones).
```plantuml
@startuml
Usuario --> (Listar Solicitudes Pendientes)
(Listar Solicitudes Pendientes)->(Agregar Sponsor) :include
(Redactar Peticion) -> (Listar Solicitudes Pendientes):include
Sponsor --> (Redactar Peticion)
@enduml
```

#### Out of Scope (casos de uso No Soportados)
Descripción...
* Caso de uso 1
* Caso de uso 2
* ...

---
## Arquitectura

### Diagramas
poner diagramas de secuencia, uml, etc
#Caso de uso Uno








### uml: class diagram
```plantuml
@startuml

@startuml

    class Usuario {
        -codigo_usuario: Integer
        -nombre: String
        -estadoApp: Boolean
        -email: String
        -localidad: NombreLocalidad
        -documento: Integer
        -telefono: Integer
        -clasificacion_documento: tipoDocumento
        +consultarLugarReciclaje()
        +registrarReciclaje()
        +visualizarMeta()
        +enviarMensaje()
        +darEstadoApp(Boolean)
        +darDocumento(Integer)
        +darTelefono(Integer)
        +cambiarEstado(): Boolean
        +cambiarLocalidad(): NombreLocalidad
        +darEmail(String)
    }

    class Administrador  {
        -nombre: String
        -codigo_administrador: Integer
        -nombre:String
        -email_app: String
        -clasificacion_documento: tipoDocumento
        -documento: Integer
        -telefono: Integer
        
        +verificarBonificacion()
        +darCodigo(Integer)
        +darEmailApp(String)
        +darDocumento(String)
        +darTelefono(Integer)
    }

    class Puntos{
        -cantidad: Integer
        +darCantidad(Integer)
        +cambiarCantidad(): Integer
    }

    class Ecopunto{
        -id_ecopunto: Integer 
        -direccion: String
        -localidad: NombreLocalidad
        +consultarKgReciclaje(Reciclaje)
        +darDireccion(String)
        +darLocalidad(NombreLocalidad)
    }

    class Reciclaje{
        -id_reciclaje: Integer
        -localidad: NombreLocalidad
        -cantidad: Integer
        +cambiarCantidad(): Integer
        +darIdReciclaje(Integer)
        +darCantidad(Integer)
        +darClasificacionReciclaje(TipoReciclaje)
    }

    Administrador "*" -- "0..1" Ecopunto : > gestiona
    Usuario "1" -- "1..*" Ecopunto : > deposita
    Usuario "0" -- "1..*" Puntos : > Tiene
    Usuario "1..*" -- "*" Reciclaje : > Tiene
    Ecopunto "*" -- "*" Reciclaje : > Tiene

    enum NombreLocalidad{
        Chapinero
        Kennedy
        Tunal
    }

    enum TipoDocumento{
        Cedula
        Pasaporte
        TarjetaIdentidad
    }

@enduml
```

### Modelo de datos
Poner diseño de entidades, Jsons, tablas, diagramas entidad relación, etc..

* Json Persona
```plantuml
@startjson
{
   "nombre":"Alvaro",
   "apellido":"Avila",
   "tipo_documento": ["CC", "PAS","TI"],
   "email":"example@hotmail.com",
   "telefono":"33212564"
}
@endjson
```
* Json Usuario
```plantuml
@startjson
{
   "codigo_usuario":"U-001",
   "nombre":"Alvaro",
   "apellido":"Avila",
   "edad":"22",
   "email":"example@hotmail.com",
   "tipo_documento": ["CC", "PAS","TI"],
   "documento":"1216546578",
   "telefono":"33212564",
   "puntos":"456",
   "estado_app":"True"
}
@endjson
```

* Json Administrador
```plantuml
@startjson
{
   "codigo_administrador":"A-001",
   "nombre":"Camila",
   "apellido":"Blanco",
   "edad":"22",
   "email_app":"example@dcapp.com",
   "tipo_documento": ["CC", "PAS","TI"],
   "documento":"1216546578",
   "telefono":"33212564"
}
@endjson
```

* Json Sponsor

```plantuml
@startjson
{
   "codigo_sponsor":"S-001",
   "nombre":"Daniel",
   "apellido":"Gantiva",
   "edad":"22",
   "email":"example@rappi.com",
   "tipo_documento": ["CC", "PAS","TI"],
   "documento":"1216546578",
   "telefono":"33212564",
   "facha_vencimiento":"22/02/2022"
}
@endjson
```

* Json Reciclaje

```plantuml
@startjson
{
   "id_reciclaje":"R-123",
   "localidad":["Kennedy","Chapinero","Tunal"],
   "cantidad":"1000"
}
@endjson
```
* Json Ecoputo

```plantuml
@startjson
{
   "id_ecopunto":"E-100",
   "localidad":["Kennedy","Chapinero","Tunal"]
}
@endjson

```

* Json CantidadPunto

```plantuml
@startjson
{
   "cantidad":"1100"
}
@endjson

```
* Json UsuarioPremium

```plantuml
@startjson
{
   "codigo_premium":"P-001",
   "nombre":"Alvaro",
   "apellido":"Avila",
   "edad":"22",
   "email":"example@hotmail.com",
   "tipo_documento": ["CC", "PAS","TI"],
   "documento":"1216546578",
   "telefono":"33212564",
   "puntos":"456",
   "fecha_vemcimiento":"20/03/2023",
   "estado_app":"True"
}
@endjson

```

---
## Limitaciones
Lista de limitaciones conocidas. Puede ser en formato de lista.
Ej.
* Llamadas del API tienen latencia X
* No se soporta mas de X llamadas por segundo
---
## Costo
Descripción/Análisis de costos
Ejemplo:
"Considerando N usuarios diarios, M llamadas a X servicio/baseDatos/etc"
* 1000 llamadas diarias a serverless functions. $XX.XX
* 1000 read/write units diarias a X Database on-demand. $XX.XX
Total: $xx.xx (al mes/dia/año)
