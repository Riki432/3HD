import os
from TextExtractor import getText
import subprocess
import shutil
from PIL import Image

# if __name__ != '__main__':
#     return
# os.chdir("/home/riki/Desktop/Study/3HD/Images")

def isImage(filename : str):
    if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
        return True
    else:   
        return False

# for f in os.listdir():
#     if isImage(f):
#         print(getText(f))

def findNameFromFile(name: str, f: str, matchWhole: bool):
    if len(name.strip()) == 0:
        raise Exception("Invalid Argument")
    words = name.split(" ")
    if not os.stat(f).st_size / 1024 > 10:
        return ""
    if isImage(f):
        text = getText(f)
        if len(text) < len(name):
            return ""
        if matchWhole:
            if(text.lower().find(name.lower()) != -1):
                return f
        else:
            if all(text.lower().find(word.lower()) != -1 for word in words):
                return f


def findNameFromFolder(name: str, folder: str, matchWhole: bool):
    '''
    Takes a name or basically keywords that are matched by text from the Images.
    If matchWhole is true, the entire word is matched at once.
    If matchWhole is false, the words are split by spaces and searched.
    '''
    

    os.chdir(folder)

    if len(name.strip()) == 0:
        raise Exception("Invalid Argument")
    words = name.split(" ")

    for f in os.listdir():
        if not os.stat(f).st_size / 1024 > 10:
            break
        if isImage(f):
            text = getText(f)
            if len(text) < len(name):
                break
            if matchWhole:
                if(text.lower().find(name.lower()) != -1):
                    return f
            else:
                if all(text.lower().find(word.lower()) != -1 for word in words):
                    return f
                
    return ""

def findNameFromFolder(name: str, folder: str, matchWhole: bool, cache):
    from Cache import storeCacheData
    '''
    Takes a name or basically keywords that are matched by text from the Images.
    If matchWhole is true, the entire word is matched at once.
    If matchWhole is false, the words are split by spaces and searched.
    '''
    os.chdir(folder)

    if len(name.strip()) == 0:
        raise Exception("Invalid Argument")
    words = name.split(" ")

    for f in os.listdir():
        if not os.stat(f).st_size / 1024 > 10:
            break
        if isImage(f):
            if cache is not None:
                _text = cache.get(f, None)
                if _text == None:
                    text = getText(f)  # This function takes a lot of time
                else:
                    text = _text[1]
                cache[f] = (os.stat(f).st_mtime, text)
            if len(text) < len(name):
                break
            if matchWhole:
                if(text.lower().find(name.lower()) != -1):
                    storeCacheData(cache)
                    return f
            else:
                if all(text.lower().find(word.lower()) != -1 for word in words):
                    storeCacheData(cache)
                    return f
    
    return ""


def findNamesFromFolder(name: str, folder: str, matchWhole: bool, cache):
    from Cache import storeCacheData
    '''
    Takes a name or basically keywords that are matched by text from the Images.
    If matchWhole is true, the entire word is matched at once.
    If matchWhole is false, the words are split by spaces and searched.
    '''
    os.chdir(folder)
    res = []
    if len(name.strip()) == 0:
        raise Exception("Invalid Argument")
    words = name.split(" ")

    dirs = os.listdir()
    for f in dirs:
        if not os.stat(os.path.join(folder ,f)).st_size / 1024 > 10:
            break
        if isImage(f):
            if cache is not None:
                _text = cache.get(f, None)
                if _text == None:
                    text = getText(f)  # This function takes a lot of time
                    cache[f] = (os.stat(f).st_mtime, text)
                else:
                    text = _text[1]
                print(os.getcwd())
                print(f)
                
            if len(text) < len(name):
                break
            if matchWhole:
                if(text.lower().find(name.lower()) != -1):
                    res.append(f)
            else:
                if all(text.lower().find(word.lower()) != -1 for word in words):
                    res.append(f)
        
        if f == dirs[-1]:
            storeCacheData(cache)
    
    return res


def sanitizeFileName(filename):
    newstring = ""
    for s in filename:
        newstring += s + "\\ "
    return newstring[0:-1]

def openFile(someFile):
    subprocess.run(["explorer", someFile])

# name = findName("Rahul Bansode", False) 
# print(name)
# openFile(name)

def copyFile(source, destination):
    shutil.copyfile(source, destination)


def copyFiles(src: str, destination: str):
    files = src.split(";")
    for f in files:
        t, name = os.path.split(f)
        try:
            shutil.copyfile(f, os.path.join(destination, name))
        except shutil.SameFileError:
            raise shutil.SameFileError
    return len(files)
