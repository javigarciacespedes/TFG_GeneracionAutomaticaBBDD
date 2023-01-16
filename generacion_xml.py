#Extraemos los elementos del xml
def extraerDatosXML(lista_elementos,root):
    for elem in root.findall('.//'):
        if "\n" not in str(elem.text) and "None" not in str(elem.text):
            if str(elem.text).isnumeric():
                lista_elementos.append(int(elem.text))
            elif str(elem.text) == "true": 
                lista_elementos.append(True)
            elif str(elem.text) == "false":
                lista_elementos.append(False)
            else:
                lista_elementos.append(str(elem.text))
    cambio = lista_elementos.pop(60)
    lista_elementos.insert(2,cambio)
    lista_elementos.insert(0,int(root.find('./tm/hk_tm_type').attrib["sequencecount"])) #Extraemos el número de secuencia (se pasa como atributo)
    lista_elementos.insert(0,"Housekeeping")

