def userEntity(item) -> dict:
  return {
    "_id" : str(item["_id"]),
    "id" : item["id"],
    "age" : item["age"],
  }

# def vaccineEntity(item) -> dict:
#   return {
#     "_id" : str(item["_id"]),
#     "id" : item["id"],
#     ""
    
#   }
def usersEntity(entity) -> list:
  return [userEntity(item) for item in entity]