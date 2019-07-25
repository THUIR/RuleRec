import sys 

def getItemEnDic(fileName, dicItems, dicPath, dicItemEn, dicEnItem):
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
	return dicItemEn, dicEnItem

def calculate_ruleFeatures(dataset, relationtype, number):

	# item id - number dictionary
	itemdic = {}
	# all items
	dicItems = {}
	item2num = {} #?
	with open('../RecData/' + dataset + '/item_dic.txt') as f:
		item2num = eval(f.readline())
		for each in item2num:
			itemdic[item2num[each]] = each

	train = {}
	with open('../RecData/' + dataset + '/train.txt') as f:
		for l in f:
			segs = l[0:-1].split(' ')
			if segs[0] not in train:
				train[segs[0]] = []
			train[segs[0]].append(itemdic[int(segs[1])])
			dicItems[itemdic[int(segs[1])]] = 0

	
	allitems = []
	for each in dicItems:
		allitems.append(each)


	f = open('../RecData/' + dataset + '/training_pairs.txt')
	training_pair = eval(f.readline())


	f = open('../RecData/' + dataset + '/usercandidates.txt')
	usercandidate = eval(f.readline())

	print('user candidate')
	print(len(usercandidate))
	print('sampleover')
		

	# Path dictionary
	dicPath = {}
	with open('../KGData/' + dataset + '/rule_score.txt') as f:
		dicPath = eval(f.readline())


	usefulrule = {}
	with open("../tempFile/"+dataset+'Temp/'+ relationtype+'_chi_'+number+'_rules.txt') as f:
		count = 0
		for l in f:
			usefulrule[l[0:-1]] = 0

	# item and entity links
	dicItemEn = {}
	dicEnItem = {}
	dicItemEn, dicEnItem = getItemEnDic('../KGData/'+dataset+'/title_entities.txt', dicItems, dicPath, dicItemEn, dicEnItem)
	dicItemEn, dicEnItem = getItemEnDic('../KGData/'+dataset+'/description_entities.txt', dicItems, dicPath, dicItemEn, dicEnItem)
	dicItemEn, dicEnItem = getItemEnDic('../KGData/'+dataset+'/brand_entities.txt', dicItems, dicPath, dicItemEn, dicEnItem)
	
	userFeature = {}
	count = 0
	for user in train:
		userFeature[user] = {}
		count += 1
		if count % 100 == 0:
			print(count)
		temp = {}
		if user not in usercandidate:
			continue
		candidates = usercandidate[user]
		for item in candidates:
			userFeature[user][item] = {}
			for r in usefulrule:
				userFeature[user][item][r] = 0
		for pre in train[user]:
			if pre not in dicItemEn:
				continue
			for s in dicItemEn[pre]:
				for end in candidates:
					if end not in dicItemEn:
						continue
					for e in dicItemEn[end]:
						if s in dicPath and e in dicPath[s]:
							for subpath in dicPath[s][e]:
								if subpath in usefulrule:
									temp[end] = 0
									userFeature[user][end][subpath] += 1
		



	training_featurepair = {}
	count = 0
	for user in train:
			training_featurepair[user] = {}
			count += 1
			if count % 100 == 0:
					print(count)
			temp = {}
			if user not in training_pair:
					continue
			candidates = training_pair[user]
			for candidate in candidates:
					for item in candidate:
							training_featurepair[user][item] = {}
							for r in usefulrule:
									training_featurepair[user][item][r] = 0
					for pre in train[user]:
							if pre == candidate[0]:
									continue
							if pre not in dicItemEn:
									continue
							for s in dicItemEn[pre]:
									for end in candidate:
											if end not in dicItemEn:
													continue
											for e in dicItemEn[end]:
													if s in dicPath and e in dicPath[s]:
															for subpath in dicPath[s][e]:
																	if subpath in usefulrule:
																			training_featurepair[user][end][subpath] += 1


	rulediction = {}
	count = 0
	for r in usefulrule:
		rulediction[r] = count
		count += 1
	fw = open("../tempFile/"+dataset+'Temp/'+relationtype+'_rulediction__chi_'+number+'.txt','w')
	fw.write(str(rulediction))
	fw.close()

	fw = open("../tempFile/"+dataset+'Temp/'+relationtype+'_feature4predict_chi_'+number+'.txt','w')
	for u in userFeature:
		for i in userFeature[u]:
			temp = str(u) + '\t' + str(item2num[str(i)]) + '\t'
			for r in usefulrule:
				temp += str(userFeature[u][i][r]) + ' '
			if len(temp.split(' ')) != 51:			
				temp = temp + '0 '
			temp = temp[0:-1] + '\n'
			fw.write(temp)

	fw.close()


	fw = open("../tempFile/"+dataset+'Temp/'+relationtype+'_feature4train_chi_'+number+'.txt','w')
	for u in userFeature:
			for i in training_featurepair[u]:
					temp = str(u) + '\t' + str(item2num[str(i)]) + '\t'
					for r in usefulrule:
							temp += str(training_featurepair[u][i][r]) + ' '
					while len(temp.split(' ')) != 51:
						temp = temp + '0 '
					temp = temp[0:-1] + '\n'
					fw.write(temp)
	fw.close()


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("error!")

	dataset = sys.argv[1]
	relationtype = sys.argv[2]#"alv"
	number = sys.argv[3]#"50"
	calculate_ruleFeatures(dataset, relationtype, number)
