import random
import sys

# global variables
dicItemEn = {}
dicEnItem = {}
dicPath = {}
dicItems = {}
train = {}

# get item to entity dic from files
def getItemEnDic(fileName, dicItemEn, dicEnItem, dicPath, dicItems):
	ccc = 0
	with open(fileName) as f:
		for l in f:
			segs = l[0:-1].split('\t')
			itemName = segs[0]
			enName = segs[2]
			if itemName not in dicItems:
				continue
			if enName not in dicPath:
				continue
			if itemName not in dicItemEn:
				dicItemEn[itemName] = {}
			if enName not in dicItemEn[itemName]:
				dicItemEn[itemName][enName] = 0
				ccc += 1
			dicItemEn[itemName][enName] += 1
			if enName not in dicEnItem:
				dicEnItem[enName] = {}
			if itemName not in dicEnItem[enName]:
				dicEnItem[enName][itemName] = 0
			dicEnItem[enName][itemName] += 1

	print(len(dicItemEn))
	print(len(dicEnItem))
	return dicItemEn, dicEnItem, dicPath, dicItems

def calculate(dataset, name, associaFile):
	train = {}
	dicItemEn = {}
	dicEnItem = {}
	dicPath = {}
	dicItems = {}

	with open(associaFile) as f:
		for l in f:
			l = l[0:-1].split('\t')
			if len(l) != 2:
				continue
			if random.random() > 0.1:
				continue
			dicItems[l[0]] = 0
			segs = l[1].split(' ')
			if l[0] not in train:
				train[l[0]] = {}
			for each in segs:
				dicItems[each] = 0
				train[l[0]][each] = 1
				if each not in train:
					train[each] = {}
				train[each][l[0]] = 1

	print(len(dicItems))

	with open('../KGData/'+dataset+'/rule_score.txt') as f:
		dicPath = eval(f.readline())

	print(len(dicPath))

	dicItemEn, dicEnItem, dicPath, dicItems = getItemEnDic('../KGData/'+dataset+'/title_entities.txt', dicItemEn, dicEnItem, dicPath, dicItems)
	dicItemEn, dicEnItem, dicPath, dicItems = getItemEnDic('../KGData/'+dataset+'/description_entities.txt', dicItemEn, dicEnItem, dicPath, dicItems)
	dicItemEn, dicEnItem, dicPath, dicItems = getItemEnDic('../KGData/'+dataset+'/brand_entities.txt', dicItemEn, dicEnItem, dicPath, dicItems)
	print(len(dicItemEn))
	print(len(dicEnItem))

	# normalization
	for each in dicItemEn:
		s = 0.0
		for k in dicItemEn[each]:
			s += dicItemEn[each][k]
		for k in dicItemEn[each]:
			dicItemEn[each][k] = 1.0 * dicItemEn[each][k] / s

	for each in dicEnItem:
		s = 0.0
		for k in dicEnItem[each]:
			s += dicEnItem[each][k]
		for k in dicEnItem[each]:
			dicEnItem[each][k] = 1.0 * dicEnItem[each][k] / s

	count = 0
	featureDic = {}
	ruleDic = {}
	for item in train:
		candidate = []
		candi = set()
		posi = len(train[item])
		if item not in dicItemEn:
			continue
		for e in dicItemEn[item]:
			for node in dicPath[e]:
				if node not in dicEnItem:
					continue
				for end in dicEnItem[node]:
					candidate.append(end)
					candi.add(end)
	
		# sampling negative training pairs
		flag = 0
		while True:
			flag += 1
			if flag > 100:
				break
			if len(train[item]) > 2 * posi or len(train[item]) == posi + len(candi):
				break
			nega = random.choice(candidate)
			if nega in train[item]:
				continue
			train[item][nega] = 0
	
		endEntity = set()
		for each in train[item]:
			if each not in dicItemEn:
				continue
			for en in dicItemEn[each]:
				endEntity.add(en)

		# searching item item paths
		for s in dicItemEn[item]:
			for end in train[item]:
				if end not in dicItemEn:
					continue
				for e in dicItemEn[end]:
					if s in dicPath and e in dicPath[s]:
						for subpath in dicPath[s][e]:
							if subpath not in ruleDic:
								ruleDic[subpath] = {}
							if item not in ruleDic[subpath]:
								ruleDic[subpath][item] = {}
							if end not in ruleDic[subpath][item]:
								ruleDic[subpath][item][end] = 0.0
							score = 1.0 * dicItemEn[item][s] * dicPath[s][e][subpath] * dicEnItem[e][end]
							ruleDic[subpath][item][end] += score
							if item not in featureDic:
								featureDic[item] = {}
							if end not in featureDic[item]:
								featureDic[item][end] = {}
							if subpath not in featureDic[item][end]:
								featureDic[item][end][subpath] = 0.0
							featureDic[item][end][subpath] += score
		if count % 1000 == 0:
			print(count)
		count += 1

	print(len(ruleDic))

	fw = open('../tempFile/'+dataset+'Temp/'+name+'_rule_dic_for_selection.txt','w')
	fw.write(str(ruleDic))
	fw.close()
	fw = open('../tempFile/'+dataset+'Temp/'+name+'_feature_dic_for_selection.txt','w')
	fw.write(str(featureDic))
	fw.close()
	fw = open('../tempFile/'+dataset+'Temp/'+name+'_selection_training_set.txt','w')
	fw.write(str(train))
	fw.close()

	total = 0
	for i in train:
	        for j in train[i]:
	                if train[i][j] == 1:
	                        total += 1


	# check if the rule meets more than 1% training pairs
	rulescore = {}
	c = 0
	for r in ruleDic:
	        c += 1
	        temp = 0
	        for s in ruleDic[r]:
	                for e in ruleDic[r][s]:
	                        if s in train and e in train[s] and train[s][e] == 1:
	                                temp += 1
	        if temp * 100 > total:
	                rulescore[r] = temp


	fw = open('../tempFile/'+dataset+'Temp/'+name+'_allrules.txt','w')
	for l in rulescore:
	        fw.write(l + '\n')
	fw.close()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Please set a dataset and a specific item association type.')
		exit()

	dataset = sys.argv[1]
	association = sys.argv[2]
	filedic = {'bav':'buy_after_view.txt', 'abu':'also_buy.txt', 'alv':'also_view.txt', 'bt':'buy_together'}
	calculate(dataset, association, '../KGData/'+dataset+'/'+filedic[association])
