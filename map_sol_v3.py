from weakref import WeakSet, WeakValueDictionary
from collections import defaultdict
# UNIQ_ID=0

class Record:
    def __init__(self, record, UNIQ_ID):
        self.record_id=UNIQ_ID
        self.record=record

class J_DB:
    def __init__(self):
        self.db=defaultdict(lambda: defaultdict(WeakSet))
        self.UNIQ_ID=0
        self.all_record=WeakSet()

    def add(self, record):
        if record.get("type",None)=="list":
            self.add_list(record)
        else:
            self._add_(self.UNIQ_ID, record)
        self.UNIQ_ID+=1
    
    def add_list(self, record):
        self.db[self.UNIQ_ID]=Record(record,self.UNIQ_ID)
        self.all_record.add(self.db[self.UNIQ_ID])
        for i in record["list"]:
            self.db["list"][i].add(self.db[self.UNIQ_ID])

    def _add_(self, UNIQ_ID, dict_):
        self.db[UNIQ_ID]=Record(dict_,UNIQ_ID)
        self.all_record.add(self.db[UNIQ_ID])
        compressed=self.compress_key(dict_)
        for key in compressed:
            self.db[key][compressed[key]].add(self.db[UNIQ_ID])

    def get(self, query):
        ret=self._get_(query)
        ret.sort()
        return [x[1] for x in ret]

    def _get_(self, query):
        if query.get("type",None)=="list":
            ret=self.get_list(query)
        else: 
            compressed=self.compress_key(query)
            db=J_DB()
            first_flag=True
            for key in compressed:
                if first_flag:
                    for record in self.db[key][compressed[key]]:
                        db._add_(record.record_id,record.record)
                    first_flag=False
                elif key in db.db:
                    db_tmp=J_DB()
                    for record in db.db[key][compressed[key]]:
                        db_tmp._add_(record.record_id,record.record)
                    db=db_tmp
                    del db_tmp
            ret=[]
            for record in db.all_record:
                ret.append((record.record_id,record.record))
            del db
        return ret

    def get_list(self, query):
        tmp=query["list"][0]
        ret=[]
        for ls in self.db["list"][tmp]:
            ret.append((ls.record_id,ls.record))
        for i in query["list"][1:]:
            tmp=ret
            ret=[]
            for ls in tmp:
                if i in ls[1]["list"]:
                    ret.append(ls)
        return ret

    def compress_key(self,record):
        ret={}
        for key in record:
            if not isinstance(record[key],dict):
                ret[key]=record[key]
            else:
                self._convert_key_([key],record[key],ret)
        return ret

    def _convert_key_(self,path,record,ret):
        for key in record:
            if not isinstance(record[key],dict):
                ret['.'.join(path)+'.'+key]=record[key]
            else:
                path.append(key)
                self._convert_key_(path,record[key],ret)
                path.pop()

    def delete(self,record):
        records=self._get_(record)
        for id,_ in records:
            del self.db[id]



if  __name__ == "__main__":
    db=J_DB()
    db.add({"last": "Doe","first":"John","active":"true","location":{"city":"Oakland","state":"CA","postalCode":"94607"}})
    db.add({"last": "Doe","first":"Lucy","active":"true","location":{"place":{"city":"Oakland","state":"CA"},"postalCode":"94607"}})
    db.add({"last": "Doe","first":"Allen","active":"true","postalCode":"94607","location":{"place":{"city":"Oakland","state":"CA"}}})
    print(db.get({"location":{"place":{"state":"CA"}},"first":"Lucy"}))
    db.delete({"location":{"place":{"state":"CA"}},"first":"Lucy"})
    print(db.get({"last":"Doe"}))
    # ReferenceError: weakly-referenced object no longer exists
    db.add({"type":"list","list":[1,2,3,4]})
    db.add({"type":"list","list":[2,3,4,5]})
    db.add({"type":"list","list":[3,4,5,6]})
    db.add({"type":"list","list":[4,5,6,7]})
    db.add({"type":"list","list":[5,6,7,8]})
    db.add({"type":"list","list":[6,7,8,9]})
    print(db.get({"type":"list","list":[2]}))
    print(db.get({"type":"list","list":[3,4]}))
    print(db.get({"type":"list","list":[1,2]}))
