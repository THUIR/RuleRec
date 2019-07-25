# RuleRec

These are our datasets and implementation for the paper:

*Weizhi Ma, Min Zhang, Yue Cao, Woojeong Jin, Chenyang Wang, Yiqun Liu, Shaoping Ma, and Xiang Ren. 2019. [Jointly Learning Explainable Rules for Recommendation with Knowledge Graph.](https://dl.acm.org/citation.cfm?id=3313607) 
In TheWebConf'19.*

**Please cite our paper if you use our datasets or codes. Thanks!**

```
@inproceedings{ma2019jointly,
  title={Jointly Learning Explainable Rules for Recommendation with Knowledge Graph},
  author={Ma, Weizhi and Zhang, Min and Cao, Yue and Jin, Woojeong and Wang, Chenyang and Liu, Yiqun and Ma, Shaoping and Ren, Xiang},
  booktitle={The World Wide Web Conference},
  pages={1210--1221},
  year={2019},
  organization={ACM}
}
```


If you have any problem about this work, you can contact Weizhi Ma (mawz12 AT hotmail.com).



## RuleRec Datasets
The constructed datasets (two scenarios: Amazon cellphone and Amazon electronic) can be found [here](https://drive.google.com/file/d/1HlfLguKR38Jd7vcYqrU-o4wxN1hpoX2x/view), which contain several parts: 

**Recommendation Data:**

train.txt, test.txt: user-item interaction data.

```
Formatting: 
	user id \t item id
```

item_dic.txt:
A python dic, key = item id in Amazon, value = item id here.


**Item Attributes:**

title.txt, brand.txt, description.txt: item attributes.

```
Formatting: 
	item id in Amazon \t the title/brand/description of this item
```
**Item Associations:**

also\_buy.txt, also\_view.txt, buy\_after\_view.txt, buy\_together.txt: item associations.

```
Formatting:
	item id in Amazon \t items that have also\_buy/also\_view/buy\_after\_view/buy\_together association with this item, split by ' '
```

**Entity Linking Data:**

title\_entities.txt, brand\_entities.txt, description\_entities.txt: entity linking results on [freebase](https://developers.google.com/freebase/).

```
Formatting:
	item id in Amazon \t entity name \t entity id in Freebase
```

**Path data:**

**KGData/\*/rule\_score.txt**: As Freebase is an extremely large knowledge graph, only the related paths in the knowledge graph are recorded in this file. The head and tail entity of each path linked by at least one item.


**training_pairs.txt** and **usercandidates.txt** are two files sampled for rule learning and recommendation. You can replace them with other sampling results. The formatting of training_pairs.txt is 'user id : [positive item id, negative item id]'.

<br/> </br>
Besides, the original Amazon datasets (including user-item interaction history and item associations) are provided by Professor Mcauley. You can download them [here](http://jmcauley.ucsd.edu/data/amazon/). 


## Rule Learning Codes

If you want to use these codes, you should download RuleRec dataset and put them together first.

**getItemItemDic.py:** Enumerate all possible rules.

**selectRules.py:** Rule selection (rule features for jointly learning will also be generated in this step).

**getFeatures.py:** Calculate features based on the selected rules for item recommendation.


Environments: Python 3.6.3

sklearn = 0.19.1

numpy = 1.13.3

```
# Example:
> python getItemItemDic.py Cellphone abu
> python selectRules.py Cellphone abu 50
> python getFeatures.py Cellphone abu 50
```


## RuleRec(BPRMF) Codes:
This implementation is based on [MyMediaLiteJava](https://github.com/jcnewell/MyMediaLiteJava). Both codes and jar file are provided.

The evaluation datasets can be downloaded from [here](https://drive.google.com/file/d/19o0BH9PI1QUTTSvmrwIphY_B9rgHszmq/view), which is generated from RuleRec Data and contains both rule selection features and rule features.

Environments: Java, version 1.6 or later


```
# Example 1: Use Cellphone dataset
> java -jar BPRMF.jar --recommender=BPRMF --training-file=./RuleRecInput/Cellphone/trainingSet.txt --test-file=./RuleRecInput/Cellphone/testSet.txt --candidateFile=./RuleRecInput/Cellphone/candidates.txt --trainingPairFile=./RuleRecInput/Cellphone/trainingPairs.txt --trainingFeatures=./RuleRecInput/Cellphone/trainingFeatures.txt --testFeatures=./RuleRecInput/Cellphone/testFeatures.txt --learningRate=0.1 --usermodel=0 --iter-times=30 --rule-weight=0.005  --ruleWeightNumber=200 --resultFile=result.txt 
# output:recall@5=0.34968 recall@10=0.48024 NDCG@10=0.28287 MRR=@100.22102 num_users=27840 num_items=100 num_lists=27840

# Example 2: Use Cellphone dataset with jointly learning
> java -jar BPRMF.jar --recommender=BPRMF --training-file=./RuleRecInput/Cellphone/trainingSet.txt --test-./RuleRecInput/Cellphone/testSet.txt --candidateFile=./RuleRecInput/Cellphone/candidates.txt --trainingPairFile=./RuleRecInput/Cellphone/trainingPairs.txt --trainingFeatures=./RuleRecInput/Cellphone/trainingFeatures.txt --testFeatures=./RuleRecInput/Cellphone/testFeatures.txt --learningRate=0.1 --usermodel=0 --iter-times=30 --rule-weight=0.005  --ruleWeightNumber=200 --resultFile=result.txt --trainTogether=2  --lossType=sigmoid --lossCombineRate=0.2 --ruleselectTrain=./RuleRecInput/Cellphone/ruleselect/ --ruleselectResult=./RuleRecInput/Cellphone/ruleselect/ 
# output:recall@5=0.36430 recall@10=0.49429 NDCG@10=0.29536 MRR=@10=0.23214 num_users=27840 num_items=100 num_lists=27840

# Example 3: Use Electronic dataset
> java -jar BPRMF.jar --recommender=BPRMF --training-file=./RuleRecInput/Electronic/trainingSet.txt --test-file=./RuleRecInput/Electronic/testSet.txt --candidateFile=./RuleRecInput/Electronic/candidates.txt --trainingPairFile=./RuleRecInput/Electronic/trainingPairs.txt --trainingFeatures=./RuleRecInput/Electronic/trainingFeatures.txt --testFeatures=./RuleRecInput/Electronic/testFeatures.txt --learningRate=0.05 --ruleWeightNumber=200 --usermodel=0 --iter-times=30 --rule-weight=0.01 --resultFile=result.txt 
# output:recall@5=0.20694 recall@10=0.29726 NDCG@10=0.17284 MRR=@10=0.13483 num_users=18223 num_items=100 num_lists=18223

# Example 4: Use Electronic dataset with jointly learning
> java -jar BPRMF.jar --recommender=BPRMF --training-file=./RuleRecInput/Electronic/trainingSet.txt --test-file=./RuleRecInput/Electronic/testSet.txt --candidateFile=./RuleRecInput/Electronic/candidates.txt --trainingPairFile=./RuleRecInput/Electronic/trainingPairs.txt --trainingFeatures=./RuleRecInput/Electronic/trainingFeatures.txt --testFeatures=./RuleRecInput/Electronic/testFeatures.txt --learningRate=0.05 --ruleWeightNumber=200 --usermodel=0 --iter-times=30 --rule-weight=0.01 --resultFile=result.txt --trainTogether=2  --lossType=sigmoid --lossCombineRate=0.005 --ruleselectTrain=./RuleRecInput/Electronic/ruleselect/ --ruleselectResult=./RuleRecInput/Electronic/ruleselect/ 
# output:recall@5=0.20798 recall@10=0.29979 NDCG@10=0.17407 MRR=@10=0.13570 num_users=18223 num_items=100 num_lists=18223
```

