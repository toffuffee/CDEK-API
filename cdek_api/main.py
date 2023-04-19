# from typing import Union,List
# from calculate import calculate
# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel,ValidationError
# import logging
# from cities  import CDEKCities

# app = FastAPI(title="Erpsmart CDEK mobile app")

# class Item(BaseModel):
#     location: str

# class Metadata(BaseModel):
#     width:int
#     height:int
#     length:int
#     weigth:int

# class Calculate(Metadata):
#     from_location: int
#     to_location: int

# class Phones(BaseModel):
#     number: str



# class Sender(BaseModel):
#     company:str
#     name:str
#     phones: List[Phones]


# class CallCurier(Metadata):
#     intake_date: str
#     intake_time_from: str
#     intake_time_to: str
#     name: str
#     comment: str
#     sender: Sender

# cdekcities = CDEKCities()





# @app.post('/cdek/cities')
# def get_Cities(item: Item):
#     try:
#         return cdekcities.get_cities_list(item.location)
#     except ValidationError as err:
#         return err
    
# @app.post('/cdek/calculate')
# def get_calculate_delivery(item: Calculate):
#     try:
#         return calculate(item.from_location,item.to_location,item.width,item.height,item.length,item.weigth)
#     except ValidationError as err:
#         return err   

# @app.post('/cdek/call')
# def call_courier(item: CallCurier):
#     try:
#         print(item)
#     except ValidationError as err:
#         return err   

# if __name__=="__main__":
#     uvicorn.run('main:app',port=8010,host='0.0.0.0',reload=True)