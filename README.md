# python-marvel

## Overview

Wrapper around the [Marvel API](http://developer.marvel.com).

## Installation

Clone the project from github.
	
    $ git clone git@iocio005/python-marvel.git
    $ cd python-marvel
    $ pip install -r requirements.txt

## How to use it?

With your [API key](http://developer.marvel.com), load..:

```python
from marvel import Marvel

public_key = 'your public_key here'
private_key = 'your private_key here'

m = Marvel.start(public_key, private_key)
```

and shoot:

```python
# list of heroes
characters = m.find_character()
# list of heroes whose names start with
characters = m.find_character('Spid')
# or one heroe
character = m.find_character('Spider-Man')
```
then, get some data about
```python
# every API call is from 20 to 20
while characters.hasNext():
	for c in characters.itemlist:
		# heroe name
		print c.name
		# heroe short description
		print c.description
		# get images from each Marvel heroe
		c.save_images()
```
if you get only one heroe...
```python
print character.name
...

```
## Changelog
### 0.0.1

**15th May 2014**

* First release.
* Wrapper around Marvel Characters

