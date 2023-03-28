class totalesDiagnostico():
    id_area = 0
    area = ""
    putaje_area = 0
    ideales = 0
    resultados = 0
    descripcion = ""

class Diagnosticos():

    categorias = []
    preguntas = []
    def __init__(self):
        
        self.categorias = self.init_categorias()
        self.preguntas = self.init_preguntas()

    def calcular_area(self,datos):
        total_resultado = []
        for categoria in self.categorias:
            codigo_categoria = categoria['id']
            totales  =  totalesDiagnostico()
            totales.id_area =codigo_categoria
            totales.area = categoria['area']
            totales.ideales = categoria['ideales']
            #recojemos las preguntas de categoria
            preguntas_arr = list(e for e in self.preguntas if e['id_categoria']  == codigo_categoria) 
            for pregunta in preguntas_arr:
                clave = pregunta['id']
                #si existe la clave en los datos
                if clave in datos:
                    totales.putaje_area = totales.putaje_area + int(datos[clave])
                else:
                    totales.putaje_area = totales.putaje_area + 0
            totales.resultados =  round( totales.putaje_area/(len(preguntas_arr)*3) * totales.ideales *100,2)
            totales.ideales = totales.ideales*100
            total_resultado.append(totales)
        totales  =  totalesDiagnostico()
        totales.area = "Total"
        for total1  in total_resultado:
            totales.putaje_area = totales.putaje_area + total1.putaje_area
            totales.ideales = totales.ideales + total1.ideales
            totales.resultados = totales.resultados + total1.resultados
        tipo_empresa = "EMPRESA D"
        if totales.resultados <= 60:
            totales.descripcion = "EMPRESA D"
        elif totales.resultados <= 70:
            totales.descripcion = "EMPRESA C"
        elif totales.resultados <= 90:
            totales.descripcion = "EMPRESA B"
        elif totales.resultados <= 100:
            totales.descripcion = "EMPRESA A"
        total_resultado.append(totales)
        return(total_resultado)
                

                


  
    
    def init_categorias(self):
        categoria = [
            {"id":1,"area":"Dirección Estratégica","ideales":0.10},
            {"id":2,"area":"Mercadeo y ventas","ideales":0.20},
            {"id":3,"area":"Madurez Digital","ideales":0.10},
            {"id":4,"area":"Gestión Financiera","ideales":0.20},
            {"id":5,"area":"Gestión de la producción","ideales":0.20},
            {"id":6,"area":"Organización y Gestión del talento humano","ideales":0.05},
            {"id":7,"area":"Legalización","ideales":0.15}
            ]
        return categoria
    

    def init_preguntas(self):
        preguntas = [
            {"id":"_1_1", "Pregunta":"1.1 ¿Tiene su empresa documentada su misión y visión?","id_categoria":1},
            {"id": "_1_2", "Pregunta":"1.2 ¿Ha documentado los valores que rigen el actuar de su empresa?","id_categoria":1},
            {"id": "_1_3", "Pregunta":"1.3 ¿Ha identificado las fortalezas, debilidades, oportunidades y amenazas para su empresa","id_categoria":1},
            {"id": "_1_4", "Pregunta":"1.4 ¿Tiene definidas las estrategias, objetivos, metas y acciones de su empresa?","id_categoria":1},
            {"id": "_1_5", "Pregunta":"1.5 ¿Planifica las actividades empresariales de corto, mediano y largo plazo","id_categoria":1},
            {"id": "_1_6", "Pregunta":"1.6 ¿Su empresa es familiar","id_categoria":1},
            {"id": "_1_7", "Pregunta":"1.7 ¿Si su empresa es familiar tiene algún plan de sucesión?","id_categoria":1},
            {"id": "_1_8", "Pregunta":"1.8 ¿El personal es tomado en cuenta en el diseño de las estrategias de su empresa?","id_categoria":1},
            {"id": "_1_9", "Pregunta":"1.9 ¿El personal es parte fundamental de las estrategias de su empresa?","id_categoria":1},
            {"id": "_1_10", "Pregunta":"1.10 ¿Conoce las ventajas competitivas de su competencia respecto a su empresa?","id_categoria":1},
            {"id": "_1_11", "Pregunta":"1.11  ¿Conoce cuáles son las tendencias de mercado para los productos y/o servicios que su empresa ofrece?","id_categoria":1},
            {"id": "_2_1", "Pregunta":"2.1 ¿Tiene definidas sus metas de crecimiento en ventas?","id_categoria":2},
            {"id": "_2_2", "Pregunta":"2.2 ¿Poseen sus productos o servicios una marca?","id_categoria":2},
            {"id": "_2_3", "Pregunta":"2.3 ¿Su marca está registrada?","id_categoria":2},
            {"id": "_2_4", "Pregunta":"2.4 ¿Está su marca diseñada e insertada en todos los elementos de publicidad gráfica y electrónica (brochures, hojas volantes, página web, etc)?","id_categoria":2},
            {"id": "_2_5", "Pregunta":"2.5 ¿Su producto o servicio ha sido diseñado de acuerdo con estudios para conocer la demanda de los clientes?","id_categoria":2},
            {"id": "_2_6", "Pregunta":"2.6 ¿Sondea los gustos y preferencias de sus clientes para mantener su producto o servicio vigente?","id_categoria":2},
            {"id": "_2_7", "Pregunta":"2.7 ¿Posee su producto o servicio una imagen comercial de acuerdo con el segmento de mercado que atiende?","id_categoria":2},
            {"id": "_2_8", "Pregunta":"2.8 ¿Su producto o servicio cuenta con los permisos necesarios para ser comercializado?","id_categoria":2},
            {"id": "_2_9", "Pregunta":"2.9 ¿Utiliza internet para ver las tendencias y nuevos diseños de productos o servicios?","id_categoria":2},
            {"id": "_2_10", "Pregunta":"2.10 ¿Conoce en detalle quién es su cliente meta?","id_categoria":2},
            {"id": "_2_11", "Pregunta":"2.11 ¿Tiene una base de datos con la información de todos sus clientes?","id_categoria":2},
            {"id": "_2_12", "Pregunta":"2.12 ¿Conoce el nivel de satisfacción de sus clientes con el servicio y/o producto que recibe de usted?","id_categoria":2},
            {"id": "_2_13", "Pregunta":"2.13 ¿Cuenta con estrategias efectivas para la captación de nuevos clientes?","id_categoria":2},
            {"id": "_2_14", "Pregunta":"2.14 ¿Tiene definido el canal o los canales de distribución para llegar a sus clientes?","id_categoria":2},
            {"id": "_2_15", "Pregunta":"2.15 ¿Conoce el nivel de rentabilidad de su canal de distribución actual?","id_categoria":2},
            {"id": "_2_16", "Pregunta":"2.16 ¿Conoce el costo de distribución de su producto o servicios?","id_categoria":2},
            {"id": "_2_17", "Pregunta":"2.17 ¿Tiene registros de las ventas de su canal de distribución?","id_categoria":2},
            {"id": "_2_18", "Pregunta":"2.18 ¿Dispone de medios efectivos para promover sus productos o servicios?","id_categoria":2},
            {"id": "_2_19", "Pregunta":"2.19 ¿Utiliza los boletines electrónicos para fidelizar clientes?","id_categoria":2},
            {"id": "_2_20", "Pregunta":"2.20 ¿Usa correo electrónico para comunicarse con los clientes?","id_categoria":2},
            {"id": "_2_21", "Pregunta":"2.21 ¿Dispone de página web para posicionar su marca y dar a conocer sus productos?","id_categoria":2},
            {"id": "_2_22", "Pregunta":"2.22 ¿Realiza un uso efectivo de redes sociales?","id_categoria":2},
            {"id": "_2_23", "Pregunta":"2.23 ¿Cuenta su empresa con presupuesto para publicidad y promoción?","id_categoria":2},
            {"id": "_2_24", "Pregunta":"2.24 ¿Cuenta la empresa con una estrategia de precios definida?","id_categoria":2},
            {"id": "_2_25", "Pregunta":"2.25 ¿Dispone de elementos correctos para la determinación de su precio de ventas?","id_categoria":2},
            {"id": "_2_26", "Pregunta":"2.26 ¿Conoce como están sus precios respecto a la competencia?","id_categoria":2},
            {"id": "_3_1", "Pregunta":"3.1 La Empresa Dispone de Computadoras","id_categoria":3},
            {"id": "_3_2", "Pregunta":"3.2 Posee dispositivos de salida (Impresoras, Fax, Parlantes)","id_categoria":3},
            {"id": "_3_3", "Pregunta":"3.3 Tiene personal capacitado para poder utilizar una computadora","id_categoria":3},
            {"id": "_3_4", "Pregunta":"3.4 Tiene sistemas operativos estandarizados (Windows, MC-OS o LINUX)","id_categoria":3},
            {"id": "_3_5", "Pregunta":"3.5 Dispone de servicio de conexión a internet","id_categoria":3},
            {"id": "_3_6", "Pregunta":"3.6 Dispone de dispositivos externos de almacenamiento (Memorias, Discos duros)","id_categoria":3},
            {"id": "_3_7", "Pregunta":"3.7 Cuentan con antivirus en las computadoras","id_categoria":3},
            {"id": "_3_8", "Pregunta":"3.8 Poseen Hosting o Dominio Web (Alojamiento en servidores web)","id_categoria":3},
            {"id": "_3_9", "Pregunta":"3.9 Tienen portal web o redes sociales de la empresa","id_categoria":3},
            {"id": "_3_10", "Pregunta":"3.10 Tienen licencias de los programas que utilizan","id_categoria":3},
            {"id": "_3_11", "Pregunta":"3.11 Tienen un plan de mantenimiento para las computadoras","id_categoria":3},
            {"id": "_4_1", "Pregunta":"4.1 ¿Conoce la rentabilidad de su negocio?","id_categoria":4},
            {"id": "_4_2", "Pregunta":"4.2 ¿Tiene el detalle del valor de los bienes materiales de su negocio?","id_categoria":4},
            {"id": "_4_3", "Pregunta":"4.3 ¿Conoce el valor de sus inventarios? (Si es de servicio elegir regular)","id_categoria":4},
            {"id": "_4_4", "Pregunta":"4.4 ¿Lleva un control de las obligaciones financieras de su empresa?","id_categoria":4},
            {"id": "_4_5", "Pregunta":"4.5 ¿Tiene detallado el registro de sus ingresos?","id_categoria":4},
            {"id": "_4_6", "Pregunta":"4.6 ¿Tiene detallado el registro de sus costos?","id_categoria":4},
            {"id": "_4_7", "Pregunta":"4.7 ¿Lleva el control detallado de sus gastos?","id_categoria":4},
            {"id": "_4_8", "Pregunta":"4.8 ¿Maneja su empresa contabilidad formal?","id_categoria":4},
            {"id": "_4_9", "Pregunta":"4.9 ¿Conoce las obligaciones fiscales aplicadas a su empresa?","id_categoria":4},
            {"id": "_4_10", "Pregunta":"4.10 ¿Lleva un control de las cuentas por cobrar que tiene su empresa?","id_categoria":4},
            {"id": "_4_11", "Pregunta":"4.11 ¿Sigue algún procedimiento para recuperar sus cuentas por cobrar?","id_categoria":4},
            {"id": "_4_12", "Pregunta":"4.12 ¿Maneja estados financieros de forma mensual?","id_categoria":4},
            {"id": "_4_13", "Pregunta":"4.13 ¿Calcula índices financieros?","id_categoria":4},
            {"id": "_4_14", "Pregunta":"4.14 ¿Tiene alguna planificación del uso de su efectivo para funcionar como empresa?","id_categoria":4},
            {"id": "_4_15", "Pregunta":"4.15 ¿Maneja alguna política para la gestión de caja chica?","id_categoria":4},
            {"id": "_4_16", "Pregunta":"4.16 ¿Está su empresa solvente de pagos?","id_categoria":4},
            {"id": "_4_17", "Pregunta":"4.17 ¿Tiene la empresa la capacidad de ser autosostenible financieramente?","id_categoria":4},
            {"id": "_4_18", "Pregunta":"4.18 ¿Conoce el nivel de ventas con el cuál cubriría sus costos variables y fijos?","id_categoria":4},
            {"id": "_4_19", "Pregunta":"4.19 ¿Tiene usted un sueldo asignado por las actividades que realiza para su empresa?","id_categoria":4},
            {"id": "_4_20", "Pregunta":"4.20 ¿Mantiene un sistema de pagos con sus proveedores?","id_categoria":4},
            {"id": "_4_21", "Pregunta":"4.21 ¿Incluye la depreciación de sus equipos en la determinación de sus costos?","id_categoria":4},
            {"id": "_5_1", "Pregunta":"5.1 ¿Conoce la capacidad de producción de su empresa?","id_categoria":5},
            {"id": "_5_2", "Pregunta":"5.2 ¿La fórmula de sus productos esta estandarizada? (Si es de servicio elegir regular)","id_categoria":5},
            {"id": "_5_3", "Pregunta":"5.3 ¿Cuenta con una base de proveedores calificada?","id_categoria":5},
            {"id": "_5_4", "Pegunta":"5.4 ¿conoce los costos de adquisición y transporte de las materias primas y otros materiales?","id_categoria":5},
            {"id": "_5_5", "Pregunta":"5.5 ¿Conoce la normativa que rige la elaboración de los productos o la prestación de los servicios que su empresa ofrece?","id_categoria":5},
            {"id": "_5_6", "Pregunta":"5.6 ¿Sus productos o servicios se elaboran considerando las normativas existentes?","id_categoria":5},
            {"id": "_5_7", "Pregunta":"5.7 ¿Las instalaciones cumplen con las normativas respectivas para su funcionamiento?","id_categoria":5},
            {"id": "_5_8", "Pregunta":"5.8 ¿Implementa buenas prácticas en sus procesos de producción o prestación de servicios?","id_categoria":5},
            {"id": "_5_9", "Pregunta":"5.9 ¿Los procesos están escritos y se aplican al momento de elaborar sus productos?","id_categoria":5},
            {"id": "_5_10", "Pregunta":"5.10 ¿Conoce cuál es el tipo de envase o empaque apropiado para el tipo de producto que elabora? (Si es de servicio elegir regular)","id_categoria":5},
            {"id": "_5_11", "Pregunta":"5.11 ¿Las viñetas y etiquetas contienen la información correspondiente a las normativas respectivas?","id_categoria":5},
            {"id": "_5_12", "Pregunta":"5.12 ¿Cuenta con el espacio adecuado para el desarrollo de la actividad a la que se dedica?","id_categoria":5},
            {"id": "_5_13", "Pregunta":"5.13 ¿Tiene desperdicios en la producción?","id_categoria":5},
            {"id": "_5_14", "Pregunta":"5.14 ¿Reutiliza los desperdicios que genera su proceso de producción?","id_categoria":5},
            {"id": "_5_15", "Pregunta":"5.15 ¿Ha determinado el periodo de caducidad de su producto?","id_categoria":5},
            {"id": "_5_16", "Pregunta":"5.16 ¿La mano de obra o su equipo de colaboradores conoce sus funciones dentro del proceso?","id_categoria":5},
            {"id": "_5_17", "Pregunta":"5.17 ¿La mano de obra o su equipo de colaboradores posee las competencias técnicas requeridas?","id_categoria":5},
            {"id": "_5_18", "Pregunta":"5.18 ¿El trabajo del operario se realiza de acuerdo a una programación?","id_categoria":5},
            {"id": "_5_19", "Pregunta":"5.19 ¿Conoce el costo del desperdicio?","id_categoria":5},
            {"id": "_5_20", "Pregunta":"5.20 ¿Aprovecha los subproductos o partes que se desperdician?","id_categoria":5},
            {"id": "_5_21", "Pregunta":"5.21 ¿Aplica controles en su proceso de producción?","id_categoria":5},
            {"id": "_5_22", "Pregunta":"5.22 ¿Tiene algún procedimiento de control de calidad?","id_categoria":5},
            {"id": "_5_23", "Pregunta":"5.23 ¿Toma en cuenta los niveles de ventas para planificar la producción?","id_categoria":5},
            {"id": "_5_24", "Pregunta":"5.24 ¿Aplica un procedimiento de costeo?","id_categoria":5},
            {"id": "_6_1", "Pregunta":"6.1 ¿Cuenta su empresa con puestos definidos de trabajo?","id_categoria":6},
            {"id": "_6_2", "Pregunta":"6.2 ¿Planea las necesidades de personal a contratar en su empresa?","id_categoria":6},
            {"id": "_6_3", "Pregunta":"6.3 ¿Realiza proceso de reclutamiento y selección de personal para su empresa?","id_categoria":6},
            {"id": "_6_4", "Pregunta":"6.4 ¿Cuentan los empleados con contratos individuales de trabajo, según las especificaciones del código de trabajo?","id_categoria":6},
            {"id": "_6_5", "Pregunta":"6.5 ¿Desarrolla y aplica programas de inducción y capacitación para sus empleados?","id_categoria":6},
            {"id": "_6_6", "Pregunta":"6.6 ¿Evalúa el desempeño de su personal?","id_categoria":6},
            {"id": "_6_7", "Pregunta":"6.7 ¿Cuenta con un manual de funciones para los empleados en sus puestos de trabajo?","id_categoria":6},
            {"id": "_6_8", "Pregunta":"6.8 ¿Cuenta su empresa con un organigrama publicado en un lugar visible para sus trabajadores?","id_categoria":6},
            {"id": "_6_9", "Pregunta":"6.9 ¿Cuenta la empresa con un reglamento interno de trabajo aprobado y publicado en un lugar visible para el trabajador?","id_categoria":6},
            {"id": "_6_10", "Pregunta":"6.10 ¿Asegura el cumplimiento de las normas de seguridad?","id_categoria":6},
            {"id": "_6_11","Pregunta":"6.11 ¿Asegura el cumplimiento de las normas salud ocupacional?","id_categoria":6},
            {"id": "_6_12", "Pregunta":"6.12 Cuentan sus empleados con prestaciones sociales de ley?","id_categoria":6},
            {"id": "_6_13", "Pregunta":"6.13 Ubica a los empleados en los puestos adecuados en base a sus capacidades?","id_categoria":6},
            {"id": "_6_14", "Pregunta":"6.14 Estimula la motivación y sana competencia de los empleados?","id_categoria":6},
            {"id": "_6_15", "Pregunta":"6.15 Tiene un plan de crecimiento para sus empleados en el mediano y largo plazo?","id_categoria":6},
            {"id": "_6_16", "Pregunta":"6.16 ¿Propicia condiciones que mejoran el entorno laboral? Por ejemplo: La comunicación, inclusión, ¿motivación?","id_categoria":6},
            {"id": "_6_17", "Pregunta":"6.17 ¿Administra sueldos y salarios para el pago de los empleados?","id_categoria":6},
            {"id": "_7_1", "Pregunta":"7.1 ¿Tiene(n) el/los empresario(s)/ socios de la empresa/ organización/ cooperativa/ RTN de Persona Natural?","id_categoria":7},
            {"id": "_7_2", "Pregunta":"7.2 ¿Está constituida legalmente la empresa/ organización/ cooperativa?","id_categoria":7},
            {"id": "_7_3", "Pregunta":"7.3 ¿Tiene la empresa/ organización/ cooperativa/ su RTN de Persona Jurídica?","id_categoria":7},
            {"id": "_7_4", "Pregunta":"7.4 ¿Tiene la empresa/ organización/ cooperativa cuenta bancaria propia (corriente/cheques)?","id_categoria":7},
            {"id": "_7_5", "Pregunta":"7.5 ¿Cuenta con sistema de facturación CAI/ Boletas de Facturación, en uso y vigente?","id_categoria":7},
            {"id": "_7_6", "Pregunta":"7.6 ¿Está registrada/ inscrita la Personalidad Jurídica: Empresa (Registro Mercantil/IP)/ organización (SDE-ODSSE)/ cooperativa (CONSUCOOP)/ empresa campesina (SAG/INA)?","id_categoria":7},
            {"id": "_7_7", "Pregunta":"7.7 ¿Está la empresa/ organización/ cooperativa: afiliada/ registrada en un organismo de integración/ representación/ otro?","id_categoria":7},
            {"id": "_7_8", "Pregunta":"7.8 ¿Está la empresa/ organización/ cooperativa afiliada y paga cotizaciones al IHSS, INFOP, RAP?","id_categoria":7},
            {"id": "_7_9", "Pregunta": "7.9 ¿Está la empresa/ organización/ cooperativa al día en la actualización de informes anuales, cambios de Junta Directiva, presentación de balances, modificación de Estatutos y de ingreso de nuevos Socios(as), otros?","id_categoria":7},
            {"id": "_7_10", "Pregunta": "7.10 ¿Tiene la empresa/ organización/ cooperativa/ permiso de operación municipal vigente?","id_categoria":7},
            {"id": "_7_11", "Pregunta": "7.11 ¿Tiene la empresa/ organización/ Cooperativa libros administrativos, contables y de actas autorizados por su ente competente?","id_categoria":7},
            {"id": "_7_12", "Pregunta": "7.12 ¿Posee Licencia Sanitaria para operar su planta? (Aplica solamente para empresas de alimentos y de interés sanitario).","id_categoria":7},
            {"id": "_7_13", "Pregunta": "7.13 ¿Su(s) producto(s) tiene(n) registro sanitario? (Aplica solamente en el caso de las empresas enfocadas en productos de interés sanitario que pueden ser fabricados, importados, envasados o expedidos).","id_categoria":7},
            {"id": "_7_14", "Pregunta": "7.14 ¿Tiene licencia ambiental para operar su negocio? (Aplica para los sectores residenciales cívicos, comerciales, industriales y recreativos).", "id_categoria":7},
            {"id": "_7_15", "Pregunta": "7.15 ¿Posee registro de marca para productos y/o servicio? (Marca: Aplica para nombres comerciales para productos y servicios para uso exclusivo).","id_categoria":7},
            {"id": "_7_16", "Pregunta": "7.16 ¿Posee patente para las invenciones de su empresa? (Patente: aplica para invenciones que pueden ser declarada con exclusividad para su explotación por el inventor).","id_categoria":7},
            {"id": "_7_17", "Pregunta": "7.17 ¿Su(s) producto(s) poseen código de barras? (Aplica para todos productos tangibles susceptibles de venta al por mayor y menor y que son inventariarles y son dispuestos al consumidor mediante envolturas, recipientes (plástico, vidrio, cartón, otros).","id_categoria":7},
            {"id": "_7_18", "Pregunta": "7.18 Posee la empresa certificado fito zoosanitario para acreditar inocuidad del producto con fines de exportación? (Aplica para productos y sub productos con fines de exportación, siempre y cuando sean de origen vegetal y animal, para control de plagas y enfermedades que puedan afectar la salud humana).","id_categoria":7},
        ]
        return preguntas
    
