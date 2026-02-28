How to Run Chopped-AI
1. <Download python> if not already (https://www.python.org/downloads/)
    Add to PATH
    Install Python Extension in VSCode
2. <Clone into master branch>
    git clone "https://github.com/ocrxn/chopped-ai"
    cd ./chopped-ai
3. <Install required dependencies>
    python3 -m pip install -r requirements.txt
    if pip install breaks, install packages manually
        python3 -m pip install <package>
4. <VENV>
    python3 -m venv venv
    ./venv/Scripts/Activate
5. <Run main.py>
    python3 main.py
    a. wait for venv source
    b. run the file again to start flask server
6. Website on port 5050 <http://127.0.0.1:5050/>


Ngrok setup
1. ngrok http 5050


git init - Initializes git for current folder
git clone - copy the whole repository
git add . - Adds all files (not including .gitignore files) for staging to commit
git pull - update local branch by pulling from origin
git commit - commits file to be commited
git push - update origin by pushing local branch
git rebase - sync origin with local and puts local changes on top for merge conflict revision
