from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# engine = create_engine('mysql+pymysql://root:chigua818@112.124.201.185/'
#                        'onlooker?charset=utf8mb4')

engine = create_engine('mysql+pymysql://root:mysql@47.110.76.95/'
                       'Bit_test?charset=utf8mb4')

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)
#
# from database.models import Dynamic,DynamicManySource,Dataorigin
# import json
# models=session.query(Dynamic).all()
# for model in models:
#
#
#
#     dy=Dataorigin()
#     print(model.id)
#     dy.dynamic_id=model.id
#     session.add(dy)
#     try:
#         session.commit()
#         print(111111)
#     except:
#         session.rollback()
#         raise Exception

