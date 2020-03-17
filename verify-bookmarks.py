#
#    Google Chrome Bookmarks check
#    ---------------------------------
#
#    This program removes dead URL in Chrome bookmarks. All removed links are stored in a separate file,
#    to keep track of them. Please note that some links may be removed for bad reasons :
#
#        - Errors 500 may be temporary
#        - Errors 403 may be valid but they can't be tested without user interaction
#        - Timeouts may also be temporary (timeout here is set to 15 seconds)
#    
#    Google Chrome Bookmarks are located in C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default.
#
#    The filename is 'Bookmark'. In order to modify it, exit from Chrome, make a copy of the file,
#    run this program, check the result and replace the result file in the original directory, before
#    relaunching Chrome.
#
#   This program only check the 'bookmark bar' and 'other bookmarks', and don't check synced bookmarks.
#


import io, os, pprint
import json, hashlib, copy
import requests

#
# Your files... 
#

original_filename = "bookmarks.json"
new_filename      = "new_bookmarks.json"
bad_filename      = "bad_bookmarks.csv"

#
# Functions
#

#----------------------------------------------
def checksum_bookmarks(bookmarks):
#----------------------------------------------

    """
        Checksum calculation
    """

    md5 = hashlib.md5()

    def checksum_node(node):

        md5.update(node['id'].encode())
        md5.update(node['name'].encode('utf-16le'))
        if node['type'] == 'url':
            md5.update(b'url')
            md5.update(node['url'].encode())
        else:
            md5.update(b'folder')
            if 'children' in node:
                for c in node['children']:
                    checksum_node(c)

    for root in roots:
        checksum_node(bookmarks['roots'][root])

    return md5.hexdigest()


#----------------------------------------------
def some_cleaning(marks, bad_file):
#----------------------------------------------

    """
        Keeps only active bookmarks

        Here we check one kind of bookmarks (either "bookmark_bar" or "other", not "synced")
    """

    result = []

    #
    # Loop over all bookmarks
    #
    
    for bkm in marks:

        if (bkm['type'] == 'url'):

            # First case: a simple url
            # ---
            
            url = bkm['url']

            
            if (url[0:4] != "http"):

                # If it's not an http bookmark => we keep it "as is"
                # ---

                status = "000"
                reason = "other"
                rok = True

            else:
                
                # else we test the connection
                # ---

                try:

                    # We test the URL with a reasonnable timeout (sometimes I found infinite loops!)
                    
                    r = requests.get(url, timeout = 15)

                    # If there's no exception, it means we got a response (good or bad)
                    
                    status = str(r.status_code)   # 
                    rok    = r.ok
                    reason = r.reason
                    
                except Exception as e:

                    # Here we have an exception, either a http response or a timeout
                    
                    status = "999"
                    rok    = False
                    reason = "Timeout/" + str(e)

            # Where are we?
            # ---
                
            print(status, rok, reason, url)

            # writes the result
            # ---
            
            if rok:

                # The result is OK so we put it in the result array
                # ---
                
                result.append(bkm)
                
            else:

                # The result is KO so we write it in the "bad_bookmarks" file in CSV format
                # ---
                
                bad_file.write("{};{};{};{};\n".format(url, status, reason, bkm['name']))

            
        elif (bkm['type'] == 'folder'):

            # Here we have a folder, without URL in it but with children (that can be other folders or bookmarks)

            folder_bookmarks = bkm['children']

            # We clean the children node
            
            bkm['children'] = some_cleaning(folder_bookmarks, bad_file)

            # ... and store the result
            
            result.append(bkm)

        else:
            
            # Unknown type: we shouldn't go here, but in case of... we keep the content unmodified.
            
            result.append(bkm)

    # That's all folk, let's return the result

    return result


#
#----------------------------------------------
#
#  Main function
#
#----------------------------------------------
#

if __name__ == "__main__":
    
    # Reads original file
    # ---

    with open(original_filename, "r", encoding="utf-8") as f:
        file_data = f.read()
        bookmarks = json.loads(file_data)

    roots = ['bookmark_bar', 'other', 'synced']

    # Prepares new bokkmark json
    # --- 

    new_bookmarks = copy.deepcopy(bookmarks)

    # Prepares trash file (bad bookmarks)
    # ---
    bad_file = open(bad_filename, "w", encoding="utf-8")

    # bookmark bar
    # ---
    bkm_bookmark_bar = bookmarks['roots']['bookmark_bar']['children']
    new_bookmarks['roots']['bookmark_bar']['children'] = some_cleaning(bkm_bookmark_bar, bad_file)

    # other favorites
    # ---
    bkm_other = bookmarks['roots']['other']['children']
    new_bookmarks['roots']['other']['children'] = some_cleaning(bkm_other, bad_file)

    # New checksum
    # ---
    chksum = checksum_bookmarks(new_bookmarks)
    new_bookmarks['checksum'] = chksum

    # Writes final file
    # ---
    new_file = open(new_filename, "w", encoding="utf-8")
    new_file.write(json.JSONEncoder().encode(new_bookmarks))
    new_file.close()

    # That's it
    # ---
    bad_file.close()
