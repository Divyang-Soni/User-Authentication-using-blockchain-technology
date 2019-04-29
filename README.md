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

##Project Dependancies

This project contains Front End part of project "User Authentication Using Blockchain Technology".

The whole project is divided in 3 parts
1) [User Interface](https://github.com/varun1524/user_authentication_blockchain_ui)
2) [Back End Server](https://github.com/divyang8842/User-Authentication-using-blockchain-technology)
3) [Blockchain Network](https://github.com/varun1524/user_authentication_blockchain_hyperledger)

In order to run the application, we need to have all 3 part of application running in the system.
