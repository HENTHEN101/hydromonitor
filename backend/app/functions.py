 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################

class DB:

    def __init__(self,Config):

        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from bson.objectid import ObjectId  
       
      
        self.Config                         = Config
        self.getcwd                         = getcwd
        self.join                           = join 
        self.floor                      	= floor 
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump  
        self.datetime                       = datetime
        self.ObjectId                       = ObjectId 
        self.server			                = Config.DB_SERVER
        self.port			                = Config.DB_PORT
        self.username                   	= parse.quote_plus(Config.DB_USERNAME)
        self.password                   	= parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError  
        self.tls                            = False # MUST SET TO TRUE IN PRODUCTION


    def __del__(self):
            # Delete class instance to free resources
            pass
 


    ####################
    # LAB 2 DATABASE UTIL FUNCTIONS  #
    ####################
    
    def addUpdate(self,data):
        '''ADD A NEW STORAGE LOCATION TO COLLECTION'''
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = remotedb.ELET2415.climo.insert_one(data)
        except Exception as e:
            msg = str(e)
            if "duplicate" not in msg:
                print("addUpdate error ",msg)
                return False
            else:                  
                return True
        
       

    def getAllInRange(self,start, end):
        '''RETURNS A LIST OF OBJECTS. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result = list(remotedb.ELET2415.climo.aggregate([{'$match': {'timestamp': {'$gte': start, '$lte': end}}}, {'$group': {'_id':0, 'humidity': {'$push': '$$ROOT.humidity'}}}, {'$project': {'max': {'$max': '$humidity'}, 'min': {'$min': '$humidity'}, 'avg': {'$avg': '$humidity'}, 'range': {'$subtract': [{'$max': '$humidity'}, {'$min': '$humidity'}]}}}]))
        except Exception as e:
            msg = str(e)
            print("getAllInRange error ",msg)            
        else:                  
            return result
       
        

    def humidityMMAR(self,start, end):
        '''RETURNS MIN, MAX, AVG AND RANGE FOR HUMIDITY. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result = list(remotedb.ELET2415.climo.aggregate([{'$match': {'timestamp': {'$gte': start, '$lte': end}}}, {'$group': {'_id':0, 'humidity': {'$push': '$$ROOT.humidity'}}}, {'$project': {'max': {'$max': '$humidity'}, 'min': {'$min': '$humidity'}, 'avg': {'$avg': '$humidity'}, 'range': {'$subtract': [{'$max': '$humidity'}, {'$min': '$humidity'}]}}}]))

           
        except Exception as e:
            msg = str(e)
            print("humidityMMAS error ",msg)            
        else:                  
            return result
        
    def temperatureMMAR(self,start, end):
        '''RETURNS MIN, MAX, AVG AND RANGE FOR TEMPERATURE. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result = list(remotedb.ELET2415.climo.aggregate([{ '$match': { 'timestamp': { '$gte': start, '$lte': end } } }, { '$group': { '_id': 0, 'temperature': { '$push': '$$ROOT.temperature' } } }, { '$project': { 'max': { '$max': '$temperature' }, 'min': { '$min': '$temperature' }, 'avg': { '$avg': '$temperature' }, 'range': { '$subtract': [ { '$max': '$temperature' }, { '$min': '$temperature' } ] } } } ]))
        except Exception as e:
            msg = str(e)
            print("temperatureMMAS error ",msg)            
        else:                 
            return result


    def frequencyDistro(self,variable,start, end):
        '''RETURNS THE FREQUENCY DISTROBUTION FOR A SPECIFIED VARIABLE WITHIN THE START AND END DATE RANGE'''
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result = list(remotedb.ELET2415.climo.aggregate([{
                            '$match': {
                            'timestamp': { '$gte': start, '$lte': end}
                            }
                        },
                     
                        {
                            '$bucket': {
                                'groupBy': f"${variable}",
                                'boundaries': list(range(101)),
                                'default': 'outliers',
                                'output': {
                                    'count': { '$sum': 1 }
                                }
                            }
                        }]))

        except Exception as e:
            msg = str(e)
            print("frequencyDistro error ",msg)            
        else:                  
            return result
        
 



def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    one = DB(Config)
 
 
    start = time() 
    end = time()
    print(f"completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()


    