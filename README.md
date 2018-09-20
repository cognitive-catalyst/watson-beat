The Watson Beat
===============

Using machine learning to spur human creativity is _so_ 2018!  Watson has used
a combination of reinforcement learning and neural networks to create the Watson Beat.

Inputs
------
 - a simple 10-20 second melody file in midi format
 - parameters for the creativity engine

Outputs
-------
 - Several layers of music in midi format that Watson created using your input
   as inspiration

Getting Started
===============
This repo, is all the code for the The Watson Beat.  It all runs locally using 
the terminal.  To run it, there are a few things you need set up on your local computer first, like python 🐍!,
and a basic familiarity with `git`.

Set you machine up for dev - if you are a first timer!
------------------------------------------------------
[Here are some directions to get your machine set up to run code](./initial_setup.md), or 
just google it!  You will also need to copy this code repository to your computer. 

Use Git
-------
To get the code on your computer you will need to `git clone` this repo.
[Here](https://guides.github.com/introduction/git-handbook/) is some great documentation on git for new comers.
Also, if you want to make contributions to the code base, we are very willing to review 
merge requests (see [forking](https://guides.github.com/activities/forking/)). 
All pull requests and commits to branches intended for release must acknowledge the
[Developer Certificate of Origin](https://elinux.org/Developer_Certificate_Of_Origin)
by including the one liner: `DCO 1.1 Signed-off-by: {Full Name} <{email address}>` (without the {})


Install Project Level Dependencies
----------------------------------
So, you just spent half an hour setting your machine up for python, and I'm telling you there is more set-up?
Yep!  Welcome to the wonderful world of code.  Open your terminal, and navigate to the directory you
created with your `git clone` command.  If you do an `ls` you should see this file, `README.md`, and the
specfic python requirements for this project are in `requirements.txt`.  
You can install the specific python packages you need for your
Watson Beat Client with the following command (again, make sure you are in this directory):

`pip install -r requirements.txt`


Ready to Run
------------
There are two main ingredients to prepare to create your song with The Watson Beat.  First, you need
a midi file with a simple melody.  Best results come when you keep this short, about 10 seconds.  Also,
leave some space between your notes to give the creativity engine some wiggle room.

The second ingredient is the `ini` file.  The `ini` file give the creativity engine all of the spices
to use, including time signature, "mood," and tempo.  [Read this to learn more about ini files](./customize_ini.md).


```
Usage:
usage: wbDev.py [-h] [-i INIFILE] [-m MIDIFILEPATH] [-o OUTPUTPATH] [-u]

optional arguments:

  -h               show this help message and exit

  -i INIFILE       Store the ini File

  -m MIDIFILEPATH  Midi File Path

  -o OUTPUTPATH    Path were all the output mid files are stored (default ./output/)

  -u               usage
```

To run, clone this git project in your filesystem if you haven't already.  Open a terminal window, navigate to the 
project home `$WB_HOME` (for example, this might be `/Users/Moe/watson-beat`)

`cd $WB_HOME/src` 

Now, in the current working directory, there is a python script that will call the code, `wbDev.py` with the
parameters you pass it. To get help, just pass it the `-h` flag:

`python wbDev.py -h`

If you pass it no paramaters, 

`python wbDev.py`

it will use the default Ini file `$WB_HOME/src/Ini/Space.ini`, the default midi
file `$WB_HOME/src/Midi/mary.mid`, and output all the files to `./output/`

To pass in specific midi and ini files use the following syntax:

`python wbDev.py -i Ini/ReggaePop.ini -m Midi/mary.mid -o /Users/Moe/midifiles/`


Putting it together
-------------------
This is where you get to have some fun! Now, you have a set of midi files, you can use your favorite 
audio tools to apply virtual instruments to the sections and mix them together into a song.  

HAPPY COMPOSING!


Video Tutorials
-------------------
[How to Change the Length of a Composition](https://www.youtube.com/watch?v=suND0biUTKQ&feature=youtu.be)

[Importing MIDI Files](https://www.youtube.com/watch?v=0mWz3h1ZiJE&feature=youtu.be)

[How to Customize Moods Part 1](https://www.youtube.com/watch?v=OUDXpJJhoK8&feature=youtu.be)

[How to Customize Moods Part 2](https://www.youtube.com/watch?v=PSqLVEJexrU&feature=youtu.be)


License
-------
See [LICENSE.txt](./LICENSE.txt)

###### Original Authors: Janani Mukundan, Jeremy Hodge, and Richard Daskas 
###### Assign Pull Requests to: amchaney

### Special note on running on Windows : you will also need to install [cygwin](https://www.cygwin.com/) as environment to run the code on. All development/testing of this code was done in *nix systems, and there is something different about the Windows shell so you need a *nix bash script emulator (which is what cygwin is). 

