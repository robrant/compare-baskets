'''
Created on 9 Sep 2014

@author: dusted-ipro

Loader for sample data --> Mongo
'''
from pymongo import MongoClient
from random import randint
import csv

def toMongo(inFile):
    '''Takes file handler and loads csv to mongo
    '''
    client = MongoClient()
    db = client.mydb
    coll = db.tescodata
    #Open the fruits and veg files
    fh = open(r'/Users/dusted-ipro/Documents/LiClipse Workspace/tesco_hack/tesco_hack/veg_clean','r')
    veg = fh.readlines()
    fh.close()
    fh = open(r'/Users/dusted-ipro/Documents/LiClipse Workspace/tesco_hack/tesco_hack/fruits_clean','r')
    fruits = fh.readlines()
    fh.close()
    #Fire at Mongo
    cnt = 0
    #number of times to run - randomised data
    lps = 5

    print 'Running'
    for lp in lps:
        print 'Duplicate Loop: ' + str(lp)
        with open(inFile, 'rb') as csvfile:
            readr = csv.reader(csvfile, delimiter=',')
            for row in readr:
                if cnt == 0:
                    #TODO: Read in the keys auto
                    pass
                else:
                    #1794234566
                    DHCARDIDRnd = int(row[0])+randint(0,1000)
                    #Date - 06-FEB-14
                    
                    doc = {'DH_CARD_ID':DHCARDIDRnd,
                            'BASKET_KEY':row[1],
                            'TRANSACTION_DATE':row[2],
                            'ITEM_QTY':int(row[3]),
                            'WEIGHT_UOM_CODE':row[4],
                            'WEIGHT_UOM_QTY':row[5],
                            'NET_SPEND':float(row[6]),
                            'VOLUME_UOM_CODE':row[7],
                            'VOLUME_UOM_QTY':row[8],
                            'TESCO_WEEK':int(row[9]),
                            'TPNB':int(row[10]),
                            'PROD_SUBGROUP':row[11],
                            'PROD_GROUP':row[12],
                            'STORE_FORMAT':row[13],
                            'SLOYALTY_HIGH':row[14],
                            'SLOYALTY_LOW':row[15]
                           }
                    #Check for fruits & veg
                    match = []
                    for v in veg:
                        if doc['PROD_GROUP'].lower() == v:
                            print v
                    for f in fruits:
                        if doc['PROD_GROUP'].lower() == f:
                            print f

                    pid = coll.insert(doc)
                doc = {}
                cnt+=1
    print 'Done: '+str(cnt)
    client.disconnect()


    return


if __name__ == '__main__':
    f = '/Users/dusted-ipro/Downloads/healthhack/01_data_extract.csv'
    toMongo(f)








