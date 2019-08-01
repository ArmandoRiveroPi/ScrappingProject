import time
from RevolicoProject.ModelBuilding import SpellCheck

start = time.time()

phrase = """Argollas tipo Versache de oro 10k--53245900 o al 76960022
76960022 o al 53245900 Lazaro Todo de oro 10k -Cadena con dige de corazon--60.00 cuc
-Argollas nevadas------------60.00 cuc
-Argollas tipo Versache------50.00 cuc 76960022 o al 53245900 Lazaro Si solicita q se lo lleven hasta la casa el servicio se cobrara aparte las tarifas son:
DE LUNES A DOMINGO
OJO:Algunos precios variaran en 1 o 2 cuc mas,en dependencia de la lejania o dificultad de acceder al lugar de destino,esto no se aplica a los municipios de 5 cuc 2 cuc:10 de octubre
3 cuc:Arroyo Naranjo,Centro Habana,Cerro,Habana Vieja,Playa,Plaza,San Miguel del Padron
4 cuc:Boyeros,Cotorro,Guanabacoa,Regla,Marianao
5 cuc:Habana del Este,La Lisa Algunos ejemplos:
1 cuc mas:Playa despues de 70 y antes del Nautico,Zamora,Electrico,San Francisco de Paula,Abel Santamaria,Los Pinos,Puente Nuevo,etc.
2 cuc mas:Managua,Santa fe,Jaimanitas,Guasimas,etc"""

corrector = SpellCheck()

print(corrector.correct_phrase(phrase))

end = time.time()
print('Took ' + str(round(end - start)) + ' seconds total')
