#from __future__ import print_function
import sqlalchemy
#from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
#from sqlalchemy import Column, Integer, String, MetaData, ForeignKey

#print(sqlalchemy.__version__)
engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
print(engine)


