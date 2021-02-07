# Proyecto Final - Bootcamp 0: #

# - CRYPTON SIMULATOR - #

## Resumen ##

Crypton Simulator es un simulador web de compra/venta de criptomonedas, en el que pueden usarse euros de forma "infinita" para realizar simulaciones de compra de criptomonedas. También pueden usarse las criptomonedas de las que dispongamos para convertirlas en euros y en el resto de criptomonedas.

El cálculo de la conversión se realiza en tiempo real vía API, a través de la plataforma CoinMarketCap. 

Las 12 criptomonedas disponibles para su uso, son:
	
- BTC: Bitcoin
- ETH: Ethereum
- XRP: XRP
- LTC: Litecoin
- BCH: Bitcoin Cash
- BNB: Binance Coin
- USDT: Tether
- EOS: EOS
- BSV: Bitcoin SV
- XLM: Stellar
- ADA: Cardano
- TRX: Tron

La aplicación esta realizada con el framework Flask de Python, y se compone de 3 páginas:

- Inicio: En el caso de que aún no se haya realizado una simulación se mostrará la información de que aún no hay movimientos y la opción mediante botón de realizar la primera simulación. En caso de haber realizado ya alguna simulación, se mostrará una tabla con el resumen de todos los movimientos (o simulaciones) realizadas.

- Simulador: En este apartado será donde podremos realizar cualquier tipo de simulación. Podemos usar Euros para comprar cualquiera de las 12 criptomonedas antes descritas, o convertir cualquiera de las criptomonedas de las que tengamos saldo a otras criptomonedas o convertirlas de nuevo en Euros.

- Estado Inversión: En esta página se muestra el estado actual de nuestras inversiones. Cada vez que se accede, se muestran los datos actualizados de: Invertido (total de euros invertidos), Valor Actual (total de euros invertidos + saldo de euros + valor actual total de todas nuestras criptomonedas en euros) y Ganancia (valor actual - invertido).

#### Restricciones: ####

- Todas las páginas tienen el mismo header y footer.
- El botón del menú correspondiente a la página en la que nos encontremos, quedará deshabilitado. Por ejemplo: estando en Inicio, no podremos usar la opción "Inicio" del menú.
- La simulación se realiza en 2 pasos: Cálculo (con el botón de la calculadora) y Realizar Operación (para guardar la simulación en la base de datos). Para realizar la simulación se lleva a cabo una validación del formulario en la que tendremos una serie de restricciones: 
	- No podremos cambiar 2 monedas iguales. Por ejemplo: 'EUR' a 'EUR'.
	- Es obligatorio introducir una cantidad en la moneda de venta.
	- La cantidad de la moneda de venta debe estar comprendida entre '0.00000001' y '1000000000'
	- El único saldo del que disponemos una cantidad infinita es de 'EUR' (Euros). El saldo de las criptomonedas dependerá de las que hayamos comprado/vendido anteriormente.
	- El botón de 'Realizar operación' estará deshabilitado mientras no hayamos realizado un cálculo con el botón correspondiente al icono de la calculadora. En caso de haber realizado un cálculo, el botón para calcular quedará deshabilitado y por contra, quedará habilitado el de 'Realizar Operación'.
	- Una vez realizado el cálculo, se mostrarán los datos de la conversión en sus correspondientes campos, pero estos quedarán deshabilitados de cara al usuario.
	- Se le ha aplicado una restricción de 60 segundos en el tiempo que pasa entre un cálculo realizado y el momento en el que queremos realizar la operación. Si pasan más de 60 segundos, no podremos realizar la operación y deberemos volver a calcular.

#### Control de Errores: ####

- Quedan controlados los posibles errores referentes a partes del código que acceden a la base de datos. En caso de error en la base de datos, se mostrarán los mensajes de error correspondientes al acceso de la base datos en cada sección o apartado donde el usuario haga uso. Además quedará un 'print' del error en la terminal para que el administrador pueda tener una referencia de dicho error.
- Así mismo y como en el caso anterior, también quedan controlados los errores referentes a la conexión vía API con CoinMarketCap, mostrando dichos errores como en el caso anteriormente expuesto.
- Además se ha personalizado la página para el típico 'Error 404', a la que se redirigiría al usuario en caso de un error en un enlace o por confusión del usuario al escribir una ruta diferente en la barra de direcciones.
- También se controla un posible 'ZeroDivisionError' que podría llegar a originarse al realizar el cálculo del precio unitario en "Simulador", dividiendo entre "0" (esto podría ocurrir por un redondeo en la cantidad de la moneda de compra, si la moneda/cantidad elegida de venta ofreciera una cantidad de compra con más de 8 decimales).

#### Características Extra: ####

- Se le ha añadido un "monedero" (con imágenes de cada moneda) con la información de los saldos de criptomonedas que tenga el usuario con una cantidad mayor que 0, y se mantiene en todo momento a la vista del usuario en cualquiera de las páginas en las que se encuentre.
- En el resumen de movimientos en la página de Inicio, al usuario se le mostrarán los precios unitarios con sus respectivas monedas (moneda de venta/moneda de compra). 
- También se controlan los números que se muestran al usuario, si los números son en notación científica, al usuario se le mostrarán en formato "float", aunque internamente se seguirá trabajando con los números en notación científica. Esto es controlado en cualquier campo en el que el usuario reciba una cantidad (inicio, simulador...).
- En Simulador, se le ha añadido como función extra el control de tiempo entre un cálculo y una operación (una vez que se quiera guardar en la base de datos). Este tiempo está impuesto en 60 segundos.
- En la página Estado Inversión, se le ha añadido un campo "Ganancias", que muestra el resultado en verde si este es positivo o en rojo si es negativo.
- Se ha personalizado una página html para el típico "Error 404".
- Se le ha añadido un favicon.ico

## Instalación ##

### Obtención de API KEY en CoinMarketCap: ###

Para que la aplicación funcione se deberá obtener una clave API en CoinMarketCap. Se puede realizar sobre la capa gratuita que ofrecen en el siguiente enlace:
[https://coinmarketcap.com/api/](https://coinmarketcap.com/api/)

### Instalación en entorno virtual: ###

Para usar el proyecto correctamente se recomienda utilizar un **entorno virtual**, para poder instalar las dependencias que requiera este proyecto. Para ello, abrimos el terminal y desde la ruta principal del proyecto escribimos la siguiente instrucción:

    python -m venv venv
Ahora deberemos **activar** el entorno que hemos creado a través de la siguiente instrucción dependiendo del sistema en el que nos encontremos:

**En Windows:**

    venv\Scripts\activate

**En Linux/Mac:**

    .venv/bin/activate


### Instalación de dependencias: ###

Ahora que ya está activado el entorno virtual y para poder usar este proyecto, necesitará instalar las distintas dependencias a través del archivo "requirements.txt". Para ello ejecutaremos la siguiente instrucción:

**Aunque no sería necesario, lo ideal sería tener nuestra versión 'pip' actualizada. Para ello ejecutamos:**

    pip install --upgrade pip

**Ahora si, instalamos las dependencias necesarias. Ejecutamos:**

    pip install -r requirements.txt

**Una vez hemos realizado estos pasos, podríamos comprobar que se han instalado correctamente todas las dependencias a traves de la siguiente instrucción:**

    pip freeze

### Creación de variables de entorno: ###

**Ahora, deberá crearse un archivo nuevo en la carpeta RAÍZ del proyecto que deberá llamar ".env" y dentro de ese fichero incluirá las siguientes variables de entorno:**

    FLASK_APP=run.py
    FLASK_ENV=development

### Creación de la base de datos: ###

Para facilitar la creación de la base de datos y teniendo en cuenta de que dispone de algún programa de gestión de bases de datos en SQLite (como: DB Browser), deberá hacer uso de la sentencia SQL para crear la tabla necesaria. 

Esta sentencia se encuentra en el archivo "initial.sql" en la ruta: 

    crypton_simulator\simulator\data\migrations\initial.sql

Esta base de datos debe crearse en la ruta del proyecto:

    simulator/data/<subasededatos>.db

### Fichero de Configuración: ###

Deberá renombrar el archivo 'config_template.py' por 'config.py' y editar el mismo con la siguiente información:

    API_KEY='Ponga aquí su API KEY de CoinMarket'
    SECRET_KEY='Ponga aquí su clave para CSRF'
    DBFILE='Ponga aquí la ruta a la base de datos'

### Ejecución: ###

Una vez realizadas las tareas anteriores, ya podrá realizar la ejecución del proyecto escribiendo a través del terminal, la siguiente instrucción:

    flask run