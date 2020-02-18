import os
from TextExtractor import getText
import subprocess
import shutil
from PIL import Image
from PySimpleGUI import Popup 

def isImage(filename : str):
    '''
    Returns true if the given filename is an image.
    For the scope of this program anyfile that ends with .png or .jpeg or .jpg is an image.
    '''
    if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
        return True
    else:   
        return False

def findNameFromFile(name: str, f: str, matchWhole: bool):
    '''
    Returns the text from an image file.
    '''
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
    Returns a list of all the files that have the text in them.
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

def findNamesFromFolder(name: str, folder: str, matchWhole: bool, cache):
    from Cache import storeCacheData
    '''
    Takes a name or basically keywords that are matched by text from the Images.
    If matchWhole is true, the entire word is matched at once.
    If matchWhole is false, the words are split by spaces and searched.
    Returns a list of all the files that have the text in them.
    '''
    os.chdir(folder)
    res = []
    if len(name.strip()) == 0:
        raise Exception("Invalid Argument")
    words = name.split(" ")
    counter = 0
    dirs = os.listdir()
    count = len(dirs)
    
    for f in dirs:
        Popup("Searching.. {}/{} files".format(counter,count), 
            auto_close=True, 
            auto_close_duration=1,
            non_blocking=True,
            no_titlebar=True,
            # title="Searching..",
            button_type=None
            )
        print("Searched {}/{} files".format(counter,count))
        counter = counter + 1
        if not os.stat(os.path.join(folder ,f)).st_size / 1024 > 10:
            continue
        if isImage(f):
            if cache is not None:
                _text = cache.get(f, None)
                if _text == None:
                    text = getText(f)  # This function takes a lot of time
                    cache[f] = (os.stat(f).st_mtime, text)
                else:
                    text = _text[1]
                
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

def openFile(someFile):
    '''
    Open a file with the default handler for that file.
    '''
    subprocess.run(["explorer", someFile])

def copyFile(source, destination):
    '''
    Takes a file name and destination name. Copies file from source to destination.
    Deprecated: Use copyFiles.
    '''
    shutil.copyfile(source, destination)


def copyFiles(src: str, destination: str):
    '''
    Takes a long string of file names seperated by ';' as source and a destination.
    Copies files from source to destinaion.
    Returns the number of files copied.
    '''
    files = src.split(";")
    for f in files:
        t, name = os.path.split(f)
        try:
            shutil.copyfile(f, os.path.join(destination, name))
        except shutil.SameFileError:
            raise shutil.SameFileError
    return len(files)

def moveFiles(src: str, destination: str):
    '''
    Takes a long string of file names seperated by ';' as source and a destination.
    Moves files from source to destinaion.
    Returns the number of files moved.
    '''
    files = src.split(";")
    for f in files:
        t, name = os.path.split(f)
        try:
            shutil.move(f, os.path.join(destination, name))
        except shutil.SameFileError:
            raise shutil.SameFileError
    return len(files)