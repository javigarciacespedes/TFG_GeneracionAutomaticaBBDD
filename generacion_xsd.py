###Función que dado un esquema, extrae todos los campos existentes del mismo
def get_columnas(esquema,lista_a_devolver):
    nodos_a_recorrer = []
    for n in esquema.iterchildren():
        nodos_a_recorrer.append(n)
    while len(nodos_a_recorrer)>0:
        nodo_actual = nodos_a_recorrer[0]
        nodos_a_recorrer = nodos_a_recorrer[1:]
        if nodo_actual.type.is_complex() or nodo_actual.type.is_list() or nodo_actual:
            for n in nodo_actual.iterchildren():
                nodos_a_recorrer.append(n)
        else:
            if nodo_actual.type.base_type:
                if str(nodo_actual.type.base_type.local_name) == 'unsignedInt' or str(nodo_actual.type.base_type.local_name) == 'integer' or str(nodo_actual.type.base_type.local_name) == 'unsignedLong' or str(nodo_actual.type.base_type.local_name) == 'float':
                    lista_a_devolver[nodo_actual.local_name] = 'Integer'
                elif str(nodo_actual.type.base_type.local_name) == 'string':
                    lista_a_devolver[nodo_actual.local_name] = 'Text'
                elif str(nodo_actual.type.base_type.local_name) == 'boolean':
                    lista_a_devolver[nodo_actual.local_name] = 'Boolean'
            else:
                if str(nodo_actual.type.local_name) == 'unsignedInt' or str(nodo_actual.type.local_name) == 'integer' or str(nodo_actual.type.local_name) == 'unsignedLong' or str(nodo_actual.type.local_name) == 'float':
                    lista_a_devolver[nodo_actual.local_name] = 'Integer'
                elif str(nodo_actual.type.local_name) == 'string':
                    lista_a_devolver[nodo_actual.local_name] = 'Text'
                elif str(nodo_actual.type.local_name) == 'boolean':
                    lista_a_devolver[nodo_actual.local_name] = 'Boolean'


###Función que selecciona los datos que queremos representar en Cassandra
def filtrado(lista_a_filtrar,filtro):
    claves = list(lista_a_filtrar.keys())
    for clave in claves:
        if clave not in filtro:
            lista_a_filtrar.pop(clave)


###Generación del script que crea la tabla en Cassandra
def generacion_tablas(columnas,datos_xml):
    file = open('aux.py','a')
    file.write("from cassandra.cqlengine.models import Model \n")
    file.write("from cassandra.cqlengine import columns\n")
    file.write("from cassandra.cqlengine.management import sync_table\n")
    file.write("from cassandra.cqlengine import connection\n")
    file.write("class housekeeping(Model): \n")
    file.write('    tm_type = columns.Text(required=True, default="Housekeeping") \n') ### No aparece en el xml ####CAMBIO PK
    file.write("    sequencecount = columns.Integer(required=True, primary_key=True) \n") ###En el xml está definida como atributo
    #file.write('    time_received = columns.Text(required=True, primary_key = True, clustering_order="DESC") \n') ### No aparece como xml
    #file.write("    tm_id = columns.BigInt(required = True) \n") ###No aparece en el xml 
    for valor in columnas:
        if valor == "current_operating_mode":
            file.write("    current_operating_mode = columns.Text(required=True) \n")
        elif valor == "current_time":
            file.write("    current_time = columns.Integer(required=True) \n")
        elif valor == "battery_status": 
            file.write("    battery_status = columns.Text(required=True) \n")
        else: 
            file.write("    {key}=columns.{value}".format(key=valor,value=columnas[valor]))
            file.write("() \n")
    file.write("connection.setup(['127.0.0.1'],'prueba', protocol_version=3) \n") ###Cambiar el nombre del keyspace prueba, por el deseado
    file.write("sync_table(housekeeping) \n")
    file.write("datos = housekeeping.create(")
    file.write("tm_type=")
    file.write("'{x}'".format(x=str(datos_xml[0])))
    file.write(",")
    file.write("sequencecount=")
    file.write(str(datos_xml[1]))
    file.write(",")
    iterador = 2
    for valor in columnas:
        if(type(datos_xml[iterador]) == str):
            file.write(valor)
            file.write("=")
            file.write("'{x}'".format(x=str(datos_xml[iterador])))
        else:
            file.write(valor)
            file.write("=")
            file.write(str(datos_xml[iterador]))
        if(iterador < len(datos_xml)+3):
            file.write(",")
        iterador = iterador+1
    file.write(") \n")
    file.close()

def crear_tabla_vacia(columnas):
    file = open('aux.py','a')
    file.write("from cassandra.cqlengine.models import Model \n")
    file.write("from cassandra.cqlengine import columns\n")
    file.write("from cassandra.cqlengine.management import sync_table\n")
    file.write("from cassandra.cqlengine import connection\n")
    file.write("class housekeeping(Model): \n")
    file.write('    tm_type = columns.Text(required=True, default="Housekeeping") \n') ### No aparece en el xml ####CAMBIO PK
    file.write("    sequencecount = columns.Integer(required=True, primary_key=True) \n") ###En el xml está definida como atributo
    #file.write('    time_received = columns.Text(required=True, primary_key = True, clustering_order="DESC") \n') ### No aparece como xml
    #file.write("    tm_id = columns.BigInt(required = True) \n") ###No aparece en el xml 
    for valor in columnas:
        if valor == "current_operating_mode":
            file.write("    current_operating_mode = columns.Text(required=True) \n")
        elif valor == "current_time":
            file.write("    current_time = columns.Integer(required=True) \n")
        elif valor == "battery_status": 
            file.write("    battery_status = columns.Text(required=True) \n")
        else: 
            file.write("    {key}=columns.{value}".format(key=valor,value=columnas[valor]))
            file.write("() \n")
    file.write("connection.setup(['127.0.0.1'],'prueba', protocol_version=3) \n") ###Cambiar el nombre del keyspace prueba, por el deseado
    file.write("sync_table(housekeeping) \n")