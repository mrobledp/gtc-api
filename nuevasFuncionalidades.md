Nueva tablas:

- Tabla paramétrica (gtc.tipo_trx_saldo) que defina para cada tipo de transacción cuál es el tipo de saldo sobre el que va a acumular los importes para la facturación
- Tabla parametrica que para cada tipo de saldo indique cuál es el porcentaje de interés, la forma de cálculo, el porcentaje que se aplica al pago mínimo y las posibles comisiones y gastos
- Tabla de acumulación de saldo (gtc.saldos_factura) que tendrá como clave el contrato, el número de extracto y el tipo de saldo y como atributos el saldo acumulado, el saldo amortizado, un campo jsonb para guardar el saldo de cada día del mes del extracto, y otro jsonb para guardar la aplicación de los pagos.
- Tabla de pagos recibidos en un contrato y extracto
- Tabla de extractos que, para cada contrato, tenga el número de extracto, la fecha de apertura, la fecha de cierre y la situación 
- Tabla de contratos que tenga el número de extracto que está abierto, más los campos tradicionales de este tipo de entidades

