import os
def clearData(author):
	os.system("rm ./%s.txt"%author)
def updateData(author,result):
	with open("./%s.txt"%author,"a") as f:
		f.write(str(result)+"\n")
def transData(author):
	with open("./%s.txt"%author,"r")as f:
		a = f.read()
	a = a.split("\n")[0:-1]
	all_count = len(a)
	win_count = a.count("1")
	lost_count = a.count("0")
	average_win = "%.2f%%"%(win_count/all_count*100)

	win_items = []
	lost_items = []

	two_win = 0 
	three_win = 0
	two_lost = 0
	three_lost = 0
	max_win = 0
	max_lost = 0 
	for index in range(all_count):
		if a[index]=="1":
			win_items.append(index)
		if a[index]=="0":
			lost_items.append(index)
	for i in range(len(win_items)):
		try:
			tmp = win_items[i+1]-win_items[i]-1
			if tmp>max_lost:
				max_lost = tmp
		except:
			pass
		try:
			if i==0:
				if win_items[i]+1 == win_items[i+1]:
					two_win+=1
			else:
				if win_items[i]+1 == win_items[i+1] and win_items[i]-1!=win_items[i-1]:
					two_win+=1
		except:
			pass

		try:
			if i==0:
				if win_items[i]+1 == win_items[i+1] and win_items[i+1]+1==win_items[i+2]:
					three_win+=1
			else:
				if win_items[i]+1 == win_items[i+1] and win_items[i]-1!=win_items[i-1] and win_items[i+1]+1 == win_items[i+2]:
					three_win+=1
		except:
			pass
	for i in range(len(lost_items)):
		try:
			tmp = lost_items[i+1]-lost_items[i]-1
			if tmp>max_win:
				max_win = tmp
		except:
			pass
		try:
			if i==0:
				if lost_items[i]+1 == lost_items[i+1]:
					two_lost+=1
			else:
				if lost_items[i]+1 == lost_items[i+1] and lost_items[i]-1!=lost_items[i-1]:
					two_lost+=1
		except:
			pass

		try:
			if i==0:
				if lost_items[i]+1 == lost_items[i+1] and lost_items[i+1]+1==lost_items[i+2]:
					three_lost+=1
			else:
				if lost_items[i]+1 == lost_items[i+1] and lost_items[i]-1!=lost_items[i-1] and lost_items[i+1]+1 == lost_items[i+2]:
					three_lost+=1
		except:
			pass
	return {"all_count":all_count,"two_win":two_win,"three_win":three_win,"two_lost":two_lost,"three_lost":three_lost,"max_win":max_win,"max_lost":max_lost,"win_count":win_count,"lost_count":lost_count,"average_win":average_win,"latest_result":a[-10:]}
