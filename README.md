<h1><img align="left" width="50" height="50" src="img/graph.gif">The Data Structures Game</h1>

The Data Structures Game is a competitive online game. The goal of this game is to help reinforce data structures concepts to students. Players will be able to take turns and test their data structures prowess as they try to free the golden node. Correctly maneuvering your way through the AVL tree will reward you with points. Test yourself against your friends, both in the lobby and on the leaderboards!


<div align="center", style="font-size: 50px">

### [:video_game: Play Now](https://data-structures-game.herokuapp.com) &emsp; [:space_invader: API](https://data-structures-game.herokuapp.com/game_board/api) &emsp; [:information_source: Wiki](https://github.com/MaksimEkin/data-structures-game/wiki)

</div>

## Developer Installation
1. [Install Anaconda](https://docs.anaconda.com/anaconda/install/)
2. Create a minimal-empty Python environment:
- ```conda create --name dsg python=3.8.5```
- ```source activate dsg```. Note that ```dsg``` is just a name. You may choose differently. The rest of the documentation assumes you named the environment ```dsg```.
3. Install [NodeJS](https://anaconda.org/conda-forge/nodejs) for React (make sure you are in ```dsg```):
- ```conda install nodejs```
4. Add the local environment variables to your path. The environment variables include the secret keys needed to run the software. **Contact the development team**
 - Mac
    - ```nano ~/.bash_profile``` and add the variables at the bottom. Close, and save.
    - ```source ~/.bash_profile``` to use the changed bash profile. 
    - ```source activate dsg``` to change it back to the virtual environment (or ```conda activate dsg```).
    - ```env``` to check the variables. It should print them on the console.
- [Windows](https://docs.oracle.com/en/database/oracle/r-enterprise/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0)
   
5. Clone the repository:
- ```git clone https://github.com/MaksimEkin/data-structures-game.git```
6. Install the libraries needed by the project using the ```requirements.txt``` located at the root directory of the project file you cloned (make sure you are on ```dsg```):
- ```pip install -r requirements.txt```
7. Install the NodeJS libraries used by React:
- ```npm install```
8. Front-end makes API requests to Heroku. When the project is run locally, this results in cross origin calls from localhost to Heroku domain.
Cross-origins calls are blocked due to a header that is in place to protect against XSS attacks. To run the code locally, you will need to change the API call url.
- Open src/Components/GameBoard.js to edit/
- Change ```const url = remote;``` with ```const url = local;```. [Code](https://github.com/MaksimEkin/data-structures-game/blob/master/src/Components/GameBoard.js#L36).
9. Build the front-end:
- ```npm run build```
10. Run from the root directory of the project:
- ```python manage.py runserver``` and visit ```http://127.0.0.1:8000```
11. If you recieve security warnings resulting from Mimetype or cross-origin, run with below instead:
- ```python manage.py runserver --insecure``` and visit ```http://127.0.0.1:8000```

## Developer Test Suites

- **Game Board API**
    - Located at [game_board/api/tests_api.py](https://github.com/MaksimEkin/data-structures-game/tree/master/game_board/api/tests_api.py)
    - Run from the root directory of the project with ```python manage.py test game_board.api.tests_api```
- **Profile Page API**
    - Located at [profile_page/api/tests_api.py](https://github.com/MaksimEkin/data-structures-game/tree/master/profile_page/api/tests_api.py)
    - Run from the root directory of the project with ```python manage.py test profile_page.api.tests_api```
- **Game Board Database**
    - Located at [game_board/database/test_db.py](https://github.com/MaksimEkin/data-structures-game/tree/master/game_board/database/test_db.py)
    - Run from the root directory of the project with ```python manage.py test game_board.database.test_db```
- **AVL Data Structure**
    - Located at [game_board/avl/test_avl.py](https://github.com/MaksimEkin/data-structures-game/blob/master/game_board/avl/test_avl.py)
    - Run from the root directory of the project with ```python manage.py test game_board.avl.test_avl```
- **Front-End Cypress Testing**
    - Located at [cypress/integration](https://github.com/MaksimEkin/data-structures-game/tree/master/cypress/integration)
    - Run using Cypress, which can be started with ```npx cypress open```
    - Once Cypress is running, select any tests that the Cypress-generated GUI displays to run them
    
[See Wiki for details.](https://github.com/MaksimEkin/data-structures-game/wiki)

