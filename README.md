# Pyrogue
Python dev rogue project


## Dependancies 
```
pygame
matplotlib
numpy
pymongo
json
```


## How to run 
Change the working directory to the Pyrogue folder and set the main.py as the script to run 

<img src="config.png" alt="config" style="zoom:150%;" />

## How to play

### Useful keys

![useful keys](useful_keys.png)

The majority of the game do not use any extra key except when you have to write your name

### On the menu 

![On the menu](menu.png)

Use <img src="keys/up.png" alt="up" style="zoom:20%;" /> <img src="keys/down.png" alt="down" style="zoom:20%;" /> and  <img src="keys/enter.png" alt="enter" style="zoom:10%;" />  to navigate and choose your option 

You may press enter to load your stats or achievement after reopening the game

### In Game

![in game](in_game.png)

Use <img src="keys/up.png" alt="up" style="zoom:20%;" /> <img src="keys/down.png" alt="down" style="zoom:20%;" /> and  <img src="keys/enter.png" alt="enter" style="zoom:10%;" />  to navigate and choose your option

In the inventory you can use your arrows to navigate between all elements and choose them with  <img src="keys/enter.png" alt="enter" style="zoom:10%;" />



### With a merchant

![merchant](merchant.png)

Use <img src="keys/up.png" alt="up" style="zoom:20%;" /> <img src="keys/down.png" alt="down" style="zoom:20%;" /> and  <img src="keys/enter.png" alt="enter" style="zoom:10%;" />  to navigate and choose your option 

### On fight

![fight](fight.png)

In the inventory you can use your arrows to navigate between all elements and choose them with  <img src="keys/enter.png" alt="enter" style="zoom:10%;" />

The sandwich need to be equipped before the fight in the inventory like the spells



## Save & Load 

The save and load is done remotely 

Be sure to have  a connection opened to the mongoDB port 27017

Fight are auto-saved for data treatment anonymously 

But saves can't be totally anonymous so we only save your mac address as a signature 

