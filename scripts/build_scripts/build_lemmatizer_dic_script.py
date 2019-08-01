import pickle

dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/RevolicoProject/ModelBuilding/lemmatization-es.txt'

dataDic = {}
with open(dataFile, 'r', encoding='utf-8') as dataF:
    for line in dataF:
        words = line.split()
        dataDic[words[1]] = words[0]

# print(dataDic['python'])

pickleString = pickle.dumps(dataDic)
outFilePath = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/RevolicoProject/ModelBuilding/lemma-dic.pickle'
with open(outFilePath, 'wb') as outFile:
    outFile.write(pickleString)
