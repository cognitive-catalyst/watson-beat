Watson Beat Developer Repo Initial Setup
========================================

#### Pre-reqs
```
python
pip
```
#### Dependencies
```
numpy
python-midi
requests
```

How to Install python on osx:

http://docs.python-guide.org/en/latest/starting/install/osx/

a) Install C compiler
```
xcode-select --install
```
b) Install homebrew
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Add the following line to the bottom of the `~/.profile` file
```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```
c) Install python
```
brew install python
```
d) check if python has been installed
```
python -V
```
This command should give you the python version

How to install pip in osx

a) `sudo easy_install pip`



How to install python in ubuntu linux:

From source: https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/

a) install dependencies
```sudo apt-get update ; sudo apt-get install build-essential checkinstall ; sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev```

b) download source
```
cd /usr/src ; wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz ; tar xzf Python-2.7.13.tgz
```
c) compile python source
```
cd Python-2.7.13

sudo ./configure

sudo make install
```
d) check the python version
```
python -V
```
This command should give you the python version

or using apt-get

a) `sudo apt-get install python2.7`

Now, go back to the [README](./README.md)

