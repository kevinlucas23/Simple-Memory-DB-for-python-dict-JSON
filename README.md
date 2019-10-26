# Simple-Memory-DB-for-python-dict-jSON-
A simple DB for python recursive dictionary, provide api for add, query and delete. Also support query for list type. The query is staple which means the element add first will come first in the return list.

```
if  __name__ == "__main__":
    db=J_DB()
    db.add({"last": "Doe","first":"John","active":"true","location":{"city":"Oakland","state":"CA","postalCode":"94607"}})
    db.add({"last": "Doe","first":"Lucy","active":"true","location":{"place":{"city":"Oakland","state":"CA"},"postalCode":"94607"}})
    db.add({"last": "Doe","first":"Allen","active":"true","postalCode":"94607","location":{"place":{"city":"Oakland","state":"CA"}}})
    print(db.get({"location":{"place":{"state":"CA"}},"first":"Lucy"}))
    #[{'active': 'true', 'last': 'Doe', 'location': {'postalCode': '94607', 'place': {'city': 'Oakland', 'state': 'CA'}}, 'first': 'Lucy'}]
    
    db.delete({"location":{"place":{"state":"CA"}},"first":"Lucy"})
    print(db.get({"last":"Doe"}))
    #[{'active': 'true', 'last': 'Doe', 'location': {'postalCode': '94607', 'city': 'Oakland', 'state': 'CA'}, 'first': 'John'}, {'active': 'true', 'postalCode': '94607', 'last': 'Doe', 'location': {'place': {'city': 'Oakland', 'state': 'CA'}}, 'first': 'Allen'}]
    
    db.add({"type":"list","list":[1,2,3,4]})
    db.add({"type":"list","list":[2,3,4,5]})
    db.add({"type":"list","list":[3,4,5,6]})
    db.add({"type":"list","list":[4,5,6,7]})
    db.add({"type":"list","list":[5,6,7,8]})
    db.add({"type":"list","list":[6,7,8,9]})
    
    print(db.get({"type":"list","list":[2]}))
    #[{'list': [1, 2, 3, 4], 'type': 'list'}, {'list': [2, 3, 4, 5], 'type': 'list'}]

    print(db.get({"type":"list","list":[3,4]}))
    #[{'list': [1, 2, 3, 4], 'type': 'list'}, {'list': [2, 3, 4, 5], 'type': 'list'}, {'list': [3, 4, 5, 6], 'type': 'list'}]
    
    print(db.get({"type":"list","list":[1,2]}))
    #[{'list': [1, 2, 3, 4], 'type': 'list'}]
```
