python3 -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp template.env .env
vim .env
touch token.json
vim token.json
