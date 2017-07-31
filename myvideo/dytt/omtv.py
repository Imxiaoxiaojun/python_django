#coding=utf-8 





# return False or True
def batchSaveTv(list):
	try:
		batchList = []
		for i in range(len(list)):
			try:
				vname = list[i].get('name')
				vurl = list[i].get('href')
				vparentid = list[i].get('parentid')
				video = models.Video(name=vname,url=vurl,parentid=vparentid,type='tv',tag='omtv',)
			except:
				logger.error('parse batchlist error')
	except:
		logger.error('EXECUTE BATCHSAVETV ERROR')	
		return False
