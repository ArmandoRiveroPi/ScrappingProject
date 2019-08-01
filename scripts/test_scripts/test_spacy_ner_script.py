import spacy
# from spacy.lang.es.examples import sentences
# from spacy import displacy
import re


def pre_process(text):
    text = str(text)
    # lowercase
    text = text.lower()
    # remove special characters and digits
    text = re.sub(r'\s+', " ", text)

    # stem
    # stemmer = SnowballStemmer('spanish')
    # tokens = word_tokenize(text)
    # stemmedTokens = [stemmer.stem(token) for token in tokens]
    # text = ' '.join(stemmedTokens)

    return text


nlp = spacy.load('es_core_news_md')
text = 'Lo mejor de lo mejor en alquiler de autos. Mabel 52637052'
text = """3 CAMIÓN CERRADO PARA CARGA Y MUDANZA (Ignacio 76429134-52683263)
alquiler de:
- camion
- brigada
Ambos o cada uno por separado."""
# text = """Hola a todos, escribo para alertar de la cantidad de ladrones, timadores y gente sin escrúpulos q hay en estos momentos anunciando ventas de perfumes originales, desde personas q dicen q si son traídos de Francia, q si ofertas de 4x100, q si originales al 80% y 100%, q si llevan más de 4 años en el negocio de la perfumería, Sí, más de 4 años engañando a la gente, Por favor no caigan en el robo de los perfumes sin cajas envueltos en nylon con la excusa q sea, son ¡¡¡REENVASADOS!!! todos, quien no ha visto en nuestro país a los q compran pomos de perfumes vacíos, pues así mismo funciona en otros países como México, Panamá, Haití y demás países q visitan los cubanos, no se dejen engañar con precios ridículamente bajos q la perfumería en TODO EL MUNDO es cara, es un abuso q vendan perfumes reenvasados q cuestan entre 2 y 3 dólares, en 30 y 40 dólares, aprovechando lamentablemente la incultura y la ignorancia de las personas en nuestro país en cuanto a perfumes. Y no sólo los perfumes reembasados, OJO TAMBIÉN CON LOS CLONES, vienen en pomos muy parecidos a los originales y en cajas sellados, provenientes de China, Rusia y Panamá, y con aromas q pueden engañar a muchos, pero YA tenemos Internet en nuestro país, busque y documentese al respecto, sepa los aspectos q debe tener un perfume original como número de serie, sello de importación, calidad del cartón de la caja y del celofán de envoltura, calidad del vidrio, entre otras muchas cosas, si ya ha sido víctima de estas personas no se quede con la duda, acuda con alguien q tenga conocimientos al respecto(En las perfumerías pudiera ser) para q vea de lo q estamos hablando.
# Espero les sea de utilidad este anuncio, y q no caigan en la trampa de tantos timadores, y desde mi humilde opinión y conocimiento hay sólo una persona sería en este negocio, en medio de tanto fraude, pero les corresponde a Uds averiguar, documentarse y dar con la persona indicada.
# Saludos a todos."""
text = """___NEBULIZADOR___ Omron__NE-C801__05-46996-82__NUEVO SIN USO__
ENVIO OPCINAL___viene c/ 3 boquillas, ESPECIFICACIONES:
Modelo: NE-C801
Tipo: Nebulizador de compresor
Especificación eléctrica (adaptador CA 100 - 240V ~ 350mA, 50/60 Hz
Especificación eléctrica (Nebulizador con compresor) 12V 0.8A
Velocidad del nebulizador aproximadamente 0.3 mL/min (sin tapa)
Tamaño de las partículas *MMAD aproximadamente 3 &#956;m (basado en EN13544-1:2007)
Capacidad del recipiente del medicamento 7 mL (cc) máx.
Cantidades adecuadas de medicamento 2 mL - 7 mL (cc)
Condiciones de operación Operación intermitente de 20 min. encendido/40 min. apagado
Temperatura de operación/Humedad: +10°C a +40°C (+50°F a 104°F),
30% a 85% de humedad relativa.
Temperatura de almacenamiento/ 20°C a +60°C (4°F a +140°F),
10% a 95% de humedad relativa
Humedad/Presión de aire 700 hPa a 1060 hPa
Peso Aprox. 270 g. (9.5 oz.) (solamente el comprensor)
Dimensiones Aprox. 142 mm (l) × 72 mm (a) × 98 mm (p) Incluye: Compresor, kit nebulizador, tubo de aire (PVC, 100 cm), tapa del filtro de aire, boquilla, filtros de aire (paquete de 5), mascarilla para adultos (PVC), mascarilla para niños (PVC), adaptador CA, estuche de almacenamiento y manual de instrucciones."""
text = pre_process(text)

doc = nlp(text)
print(doc.text)
print('POS Tokens', '>'*50)
for token in doc:
    if token.pos_ == 'NOUN' or token.pos_ == 'ADJ':
        print(token.text, token.pos_, token.dep_)

print('ENTITIES', '>'*50)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

# displacy.serve(doc, style='ent')
