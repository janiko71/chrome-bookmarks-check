# chrome-bookmarks-check
Check your Google Chrome Bookmarks and remove dead links. This program removes dead URL in Chrome bookmarks. All removed links are stored in a separate file, to keep track of them. Please note that some links may be removed for bad reasons :

- Errors 500 may be temporary
- Errors 403 may be valid but they can't be tested without user interaction
- Timeouts may also be temporary (timeout here is set to 15 seconds)
  
Google Chrome Bookmarks are located in C:\Users\\{user}\AppData\Local\Google\Chrome\User Data\Default.

The filename is 'Bookmark'. In order to modify it, exit from Chrome, make a copy of the file, run this program, check the result and replace the result file in the original directory, before relaunching Chrome.

This program only check the 'bookmark bar' and 'other bookmarks', and don't check synced bookmarks.

# Some cleaning
As usual, Google knows everything from you. Even if you stop synchronization and delete all the Bookmarks files on all your devices, your favorites will absurdly reappear. To prevent this, go https://chrome.google.com/sync and reset your datas (= there are somewhere in Google's cloud...).

Source : https://support.google.com/chrome/thread/7732182?hl=en
