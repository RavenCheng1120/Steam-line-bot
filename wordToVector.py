from gensim.models import word2vec
import jieba
import numpy as np
import json
from scipy.linalg import norm

def findAnswer(inputline):
	#載入word2vec模型
	wiki_model = word2vec.Word2Vec.load("w2v-80.model")

	#載入json檔案，內含30則問答訊息
	with open('QandA.json', 'r') as f:
		jsonfile = json.load(f)

	readText = []
	for line in jsonfile:
		readText.append(line['Question'])


	#計算Question的句向量
	splitText = []
	senVector = []

	for i in readText:
		tempVec = np.zeros((80, ), dtype='float64')
		count = 0
		#切割預設Q&A的問題句子
		splitText = jieba.cut(i, cut_all=False)
		for word in splitText:
			if wiki_model.wv.__contains__(word):
				count = count + 1
				tempVec += wiki_model.wv.__getitem__(word)
		# 總句向量 / 該句出現過的詞彙數
		tempVec = tempVec/count
		senVector.append(tempVec)
	senVector = np.array(senVector)

	#np.save('Question_vector',senVector)
	#senVector=np.load("Question_vector.npy")


	#計算輸入句子的句向量
	tempVec = np.zeros((80, ), dtype='float64')
	count = 0
	splitText = jieba.cut(inputline, cut_all=False)
	for word in splitText:
		if wiki_model.wv.__contains__(word):
			count = count + 1
			tempVec += wiki_model.wv.__getitem__(word)
	# 總句向量 / 該句出現過的詞彙數
	tempVec = tempVec/count
	tempVec = np.array(tempVec)

	#計算與輸入句子最相似的Question句向量，用夾角餘弦值計算
	similar_num=0
	max_num = np.dot(senVector[0], tempVec) / (norm(senVector[0]) * norm(tempVec))
	for i in range(len(jsonfile)):
		temp = np.dot(senVector[i], tempVec) / (norm(senVector[i]) * norm(tempVec))
		if(temp > max_num):
			max_num = temp
			similar_num = i
	#print(np.dot(senVector[0], senVector[1]) / (norm(senVector[0]) * norm(senVector[1])))
	#print(inputline)
	#print(jsonfile[similar_num]['Answer'])
	#print(max_num)
	return jsonfile[similar_num]['Answer']


#inputline = "遊戲不小心刪掉了怎麼辦？可以重新下載嗎？"
#result = findAnswer(inputline)