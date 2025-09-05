# To launch the app with a starter script and a vfs connected
python "main.py" --vfs VFS.json --script startup.txt

# To pull a certain commit
git fetch origin {copied SSH of the commit}
git checkout FETCH_HEAD