from RevolicoProject.ModelBuilding import TfidfProvider
from RevolicoProject.functions import dict_average
import time
start = time.time()

dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump.csv'

tfidf = TfidfProvider()

# tfidf.build_model(dataFile, amount=0)

text = 'LAVADORA LG INVERTER CARGA FRONTAL 12KG.76440658,52938688'
term = 'lavadora'
doc = """LAVADORA LG CARGA FRONTAL 12KG TECNOLOGIA INVERTER ...950CUC LAVADORA LG INVERTER AUOMATICA COLOR BLANCA 12KG ...750CUC,, SPLIT 1 TMARCA TAKESHY CON TUBERIAS DE COBRE. LLAMAR AL> 76440658 o 52938688 con SERGIO PUBLICADO POR PUBLIDEA (Publicista dan) ******SI DESEA PUBLICAR ANUNCIOS EN REVOLICO CONTACTE A LA AGENCIA PUBLIDEA AL TELEFONO 78356727*******
correo:[email protected]"""

termTfidf = tfidf.get_term_tfidf(doc, term)
print(term, termTfidf)

textTfidf = tfidf.get_text_tfidf(doc, text)
print(textTfidf)

totalTfidf = tfidf.get_text_tfidf(doc, doc)
print('Total Average:', dict_average(totalTfidf))

end = time.time()
print('Took', end - start, 'seconds')
