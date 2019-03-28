# Steps to setup environment locally
## install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

## install python3
brew install python3

## create virtual env
python3 -m venv venv3

## run python 3 virtual env
source ~/venv3/bin/activate

## install pip package in Virtual Env
pip install -r requirements.txt