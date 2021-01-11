def checkText(path):
    list_ = []
    with open(path, 'r') as tf:
        list_ = tf.read().split('$')
        try:
            list_.remove("")
        except:
            pass
    return list_


def checkDuplicate(link_list):
    import collections

    uniq = []
    for item, count in collections.Counter(link_list).items():
        if count > 1:
            uniq.append(item)
    return uniq

def checkUnDownloaded():
    folder = 'text/'
    archive_path = folder+"YacLinkArchive.txt"
    used_path = folder+"YacLinkUsed.txt"
    started_path = folder+"YacStarted.txt"
    downloaded_path = folder+"YacDownloaded.txt"
    invalid_path = folder+ "Invalid.txt"

    downloaded_list = []
    started_list = []
    with open(started_path, 'r') as tf:
        started_list = tf.read().split('$')
        try:
            started_list.remove("")
        except:
            pass
    with open(downloaded_path, 'r') as tf:
        downloaded_list = tf.read().split('$')
        try:
            downloaded_list.remove("")
        except:
            pass
        
    #not_downloaded = list(set(started_list)-set(downloaded_list))    
    not_downloaded = list(set(downloaded_list)-set(started_list))    

    return not_downloaded

