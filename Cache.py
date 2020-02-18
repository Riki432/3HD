import json
import os

Cache_Path = "C:\\Users\\banso\AppData\\Local\\Temp"

def clearCache():
    if(os.path.exists(os.path.join(Cache_Path, ".data.json"))):
        os.remove(os.path.join(Cache_Path, ".data.json"))
        return True
    else:
        return False


def cleanCache(folder: str):
    #Real Files = ("Some Date", "File Name")
    #Cache Files = ("Some Date", "File Name")
    real_files_names = os.listdir(folder)
    real_files = dict()
    cache_files = getCacheData()
    for name in real_files_names:
        if not cache_files.get(name, None) == None:
            if not cache_files.get(name)[0] == os.stat(os.path.join(folder, name)).st_mtime:
                cache_files.pop(name)
    # storeCacheData(cache_files)
    return cache_files



def storeCacheData(table):    
    with open(os.path.join(Cache_Path, ".data.json"), "w+") as fp:
        json.dump(table, fp, indent=True)
    
def getCacheData(): 
    os.chdir(Cache_Path)   
    try: 
        with open(".data.json", "r") as fp:
            data = json.load(fp)
            # keys = data.keys() 
            # # print(keys)
            # while(len(keys) > 1000):
            #     data.popitem()
            #     keys = data.keys()
            # with open(".data.json", "w") as fp:
            #     json.dump(data, fp, indent=True)
            return data
    except FileNotFoundError:
        return dict()

