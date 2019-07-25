import numpy as np
import sys
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import linear_model



def selection(dataset, association, number):
	# category = "bt"
	
	# Read in data
	usefulrule = {}
	count = 0
	with open("../tempFile/"+dataset+'Temp/' + association + '_allrules.txt') as f:
		for l in f:
			usefulrule[l[0:-1]] = count
			count += 1

	train = {}
	with open("../tempFile/"+dataset+'Temp/' + association + '_selection_training_set.txt') as f:
		train = eval(f.readline())

	path = {}
	with open("../tempFile/"+dataset+'Temp/' + association + '_feature_dic_for_selection.txt') as f:
		path = eval(f.readline())

	# calculate features for rule selection
	vlen = len(usefulrule)
	trainingset = []
	output = []
	count = 0
	for s in train:
		count += 1
		if count % 1000 == 0:
			print(count)
		for e in train[s]:
			temp = []
			if s in path and e in path[s]:
				for r in usefulrule:
					if r in path[s][e]:
						temp.append(path[s][e][r])
					else:
						temp.append(0.0)
			else:
				continue
			if len(temp) != vlen:
				print("error")
				break
			trainingset.append(temp)
			output.append(train[s][e])


	rulename = {}
	ruleid = {}
	count = 0
	for r in usefulrule:
		ruleid[count] = []
		rulename[count] = r
		count += 1

	for u in trainingset:
		for i in range(0,len(u)):
			ruleid[i].append(u[i])

	ruleNumber = number
	if number > len(usefulrule):
		ruleNumber = 'all'

	chi = SelectKBest(chi2, k=ruleNumber).fit_transform(trainingset, output)
	goodchi = {}
	for k in range(0,len(chi)):
		goodchi[k] = []
	for u in chi:
		for i in range(0,len(u)):
			goodchi[i].append(u[i])


	selectedRules = {}
	fw = open("../tempFile/"+dataset+'Temp/'+ association+'_chi_'+str(number)+'_rules.txt', 'w')
	for r in ruleid:
		flag = 0
		for k in goodchi:
			if ruleid[r] == goodchi[k]:
				flag = 1
				selectedRules[rulename[r]] = r
				break
		if flag == 1:
			fw.write(rulename[r] + '\n')

	fw.close()

	# get the name of each edge
	edge = {}
	with open('../KGData/' + dataset + '/relation_dic.txt') as f:
		edge = eval(f.readline())

	edic = {}
	for each in edge:
		edic[edge[each]] = each


	fw = open("../tempFile/"+dataset+'Temp/'+association + '_chi_'+str(number)+'_rulenames.txt','w')
	for r in selectedRules:
		segs = r.split(' ')
		temp = ""
		for i in range(0, len(segs) - 1):
			temp += edic[int(segs[i])] + ' '
		fw.write(temp[0:-1] + '\n')

	fw.close()


	# calculate features for jointly learing 
	vlen = len(selectedRules)
	trainingset = []
	output = []
	count = 0
	for s in train:
		count += 1
		if count % 1000 == 0:
			print(count)
		for e in train[s]:
			temp = []
			if s in path and e in path[s]:
				for r in selectedRules:
					if r in path[s][e]:
						temp.append(path[s][e][r])
					else:
						temp.append(0.0)
			else:
				continue
			if len(temp) != vlen:
				print("error")
				break
			trainingset.append(temp)
			output.append(train[s][e])

	fw = open("../tempFile/"+dataset+'Temp/x_' + association + '_' + str(number) + '.txt','w')
	for f in trainingset:
		temp = ""
		for each in f:
			temp += str(each) + ' '
		while len(temp.split(' ')) != 51:
			temp += '0 '
		fw.write(temp[0:-1] + '\n')
	fw.close()

	fw = open("../tempFile/"+dataset+'Temp/y_'+association + '_' + str(number) + '.npy','w')
	for f in output:
		fw.write(str(f) + '\n')
	fw.close()

#	trainArray = np.array(trainingset)
#	np.save('x_' + category + '_' + str(number) + '.npy', trainArray)
#	outputArray = np.array(output)
#	np.save('y_'+category + '_' + str(number) + '.npy', outputArray)


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print('Please set a specific item association type and rule number.')
		exit()

	dataset = sys.argv[1]
	association = sys.argv[2]
	number = int(sys.argv[3])
	selection(dataset, association,  number)

