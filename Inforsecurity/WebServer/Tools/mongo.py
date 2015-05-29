import pymongo
from bson.objectid import ObjectId
import random
import datetime
connection = pymongo.MongoClient("221.2.164.60", 27017)
db = connection.InfoSecurity
nowtime = datetime.datetime.now()
for i in range(10000):
	tmpdict = {
		'pc_id': ObjectId('50dd84821eb16c0c9257f1ca'), 
		'riskvalue': random.randint(0,100) , 
		'user_id': ObjectId('50d1a8891eb16c2c28644f3b'), 
		'datetime': nowtime-datetime.timedelta(seconds=60*i)
	}
	db.pc_assess.save(tmpdict)

print db.pc_assess.find()