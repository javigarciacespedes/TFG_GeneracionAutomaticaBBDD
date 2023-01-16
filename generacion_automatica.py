import os
from subprocess import call
import xml.etree.ElementTree as ET
import xmlschema
import generacion_xml
import generacion_xsd

#MAIN

###Declaración de variables
telemetria = []  #Contiene los datos del xml 
columnas_tabla = {} #Contiene los datos del esquema: Nombre de columnas y 
schema = "" #Contiene el nombre del esquema  

###Importamos el esquema
fileDir = os.getcwd()
fileExt = ".xsd"

for xsd in os.listdir(fileDir):
    if xsd.endswith(fileExt):
        schema = xmlschema.XMLSchema(xsd)

###Seleccionamos los campos que queremos extraer del esquema. Housekeeping
filter = ['tm_type','sequencecount','time_received','tm_id','current_operating_mode','current_time',
'battery_status','das_p3v','das_p5v','das_p15v','das_n15v','pdu_p3v3','pdu_p5v','mgm1_p5v','mgm2_p5v','mgm3_p15v',
'mgm3_n15v','mgt_x_vbus','temp_a_p5v','temp_b_p5v','modem_vbus','rw_p5v','rw_vbus','mts_vbus','boom1_vbus','boom2_vbus',
'ttc_stat','sma_sb01','sma_sb02','batt_tbat1_tm','batt_tbat2_tm','batt_tbat3_tm','batt_vbus_tm','batt_vbat_tm','psu_t_tm',
'p3v3_tm','p5v_tm','p15v_tm','n15v_tm','psu_ip5v_tm','psu_ip15v_tm','psu_in15v_tm','psu_ip3v3_tm','pdu_ivbus_tm',
'pv_tpsxp_tm','pv_tpsxn_tm','pv_tpsyp_tm','pv_tpsyn_tm','pv_tpszp_tm','pv_ispxp_tm','pv_ispxn_tm','pv_ispyp_tm',
'pv_ispyn_tm','pv_ispzp_tm','obc_t_tm','mgm1_t_tm','mgm2_t_tm','mgm3_t_tm','mgm1_x_tm','mgm1_y_tm','mgm1_y_tm',
'mgm1_z_tm','mgm2_x_tm','mgm2_y_tm','mgm2_z_tm','mgm3_x_tm','mgm3_y_tm','mgm3_z_tm','mgt_tx_tm','modem_t_tr_tm',
'ebox_t_int_tm','ebox_t_ext_tm','batt_t_ext_tm','batt_t_int_tm','ss6_xp_tm','ss6_xn_tm','ss6_yp_tm','ss6_yn_tm','ss6_zp_tm',
'ss6_zn_tm','rw1_t_tm','rw2_t_tm','mts_p1tts1_tm','mts_p1tts2_tm','mts_p1tts3_tm','mts_p1tts4_tm','mts_p1tts5_tm','mts_p1tts6_tm']

#Extraemos del esquema XSD los datos referentes a las columnas
generacion_xsd.get_columnas(schema,columnas_tabla)  
generacion_xsd.filtrado(columnas_tabla,filter)


fileDir = os.getcwd()
fileExt = ".xml"

#Procesamos los ficheros XML 
for xml in os.listdir(fileDir):
    if xml.endswith(fileExt):
        tree = ET.parse(xml)
        root = tree.getroot()
        generacion_xml.extraerDatosXML(telemetria,root)
        generacion_xsd.generacion_tablas(columnas_tabla,telemetria)
        exec(open("aux.py").read())
        call(['rm','aux.py'])
        call(['rm',xml])
        telemetria = []
    else: 
        generacion_xsd.crear_tabla_vacia(columnas_tabla)
        call(['rm','aux.py'])
print("Telemetría insertada de manera correcta.")
