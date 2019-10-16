#!/bin/bash
pyenv global system 3.6
pip3 install --upgrade pip
pip3 install pylint
pip3 install -r requirements.txt
python3 setup.py install
wget https://github.com/typesupply/vanilla/archive/master.zip
unzip master.zip
cd vanilla-master
python3 setup.py install
cd ..
rm master.zip
rm -r vanilla-master
wget https://github.com/typesupply/defconAppKit/archive/master.zip
unzip master.zip
cd defconAppKit-master
python3 setup.py install
cd ..
rm master.zip
rm -r defconAppKit-master
wget https://github.com/typesupply/compositor/archive/master.zip
unzip master.zip
cd compositor-master
python3 setup.py install
cd ..
rm master.zip
rm -r compositor-master
wget https://github.com/PageBot/PageBotCocoa/archive/master.zip
unzip master.zip
cd PageBotCocoa-master
python3 setup.py install
cd ..
rm master.zip
rm -r PageBotCocoa-master
wget https://github.com/typemytype/drawbot/archive/master.zip
unzip master.zip
cd drawbot-master
python3 setup.py install
cd ..
rm master.zip
rm -r drawbot-master
