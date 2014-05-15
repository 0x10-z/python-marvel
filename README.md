# python-marvel

## Overview

Wrapper around the [Marvel API](http://developer.marvel.com).

## Installation

Clone the project from github.
	
    $ git clone git@iocio005/python-marvel.git
    $ cd python-marvel
    $ pip install -r requirements.txt

## How to use it?

With your API KEY, load...:

```python
from marvel import Marvel

public_key = 'your public_key here'
private_key = 'your private_key here'

m = Marvel.start(public_key, private_key)
```

and shoot:

```python
# list of characters
characters = m.find_character()
# list of characters whose names start with
characters = m.find_character('Spid')
# or one character
character = m.find_character('Spider-Man')
```
then, get some data about
```python
while characters.hasNext(): # every api call 20 to 20
	for c in characters.itemlist:
		print c.name # name
		print c.description # short description about
		c.save_images() # get images from each Marvel character
```
if you find one character...
```python
print character.name
...

```
## Changelog
### 0.0.1

**15th May 2014**

* First release.
* Wrapper around Marvel Characters

