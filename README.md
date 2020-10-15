<h1><img align="left" width="50" height="50" src="img/graph.gif">The Data Structures Game</h1>

The Data Structures Game is a competitive online game. The goal of this game is to help reinforce data structures concepts to students. Players will be able to take turns and test their data structures prowess as they try to free the golden node. Correctly maneuvering your way through the AVL tree will reward you with points. Test yourself against your friends, both in the lobby and on the leaderboards!


<div align="center", style="font-size: 50px">

### [:video_game: Play Now](https://data-structures-game.herokuapp.com) [:space_invader: API](https://data-structures-game.herokuapp.com/game_board/api) [:information_source: Wiki](https://github.com/MaksimEkin/data-structures-game/wiki)

</div>

## Developer Installation
1. Install Anaconda ([Reference](https://docs.anaconda.com/anaconda/install/))
2. Create a minimal-empty Python environment:
- ```conda create --name dsg python=3.8.5```
- ```source activate dsg```. Note that ```dsg``` is just a name. You may choose differently. The rest of the documentation assumes you named the environment ```dsg```.
3. Install [NodeJS](https://anaconda.org/conda-forge/nodejs) for React:
- ```conda install -c conda-forge nodejs```
4. Add the local environment variables to your ```.bash_profile``` (Called System Variables on Windows). **Contact the development team**
5. Clone the repository. Don’t forget to checkout to the ```develop``` branch. Checkout from ```develop``` to a new branch if implementing new features. 
- ```git clone https://github.com/MaksimEkin/data-structures-game.git```
6. Install the libraries needed by the project using the ```requirements.txt``` located at the root directory of the project file you cloned (make sure you are on ```dsg```).
- ```pip install -r requirements.txt```
7. Install the NodeJS libraries used by React
- ```npm install```
8. Run from the root directory of the project
- ```python manage.py runserver``` and visit ```http://127.0.0.1:8000```

[See Wiki for details.](https://github.com/MaksimEkin/data-structures-game/wiki)