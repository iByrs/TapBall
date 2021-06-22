# TapBall
![alt text](https://github.com/iByrs/TapBall/blob/master/docs/img/TapBall_Logo.jpeg)
## Introduction 
TapBall is a university project made by student Vincent Pastor (X81000834) from the University of Catania. The idea was born in occasion of UEFA Euro 2020, as indeed the project consist of trying to predict in real time the winning chance of the competing teams during the match.
## Architecture
![alt text](https://github.com/iByrs/TapBall/blob/master/docs/img/Architecture.jpg)
### For more information about the technologies I used, please read the project documentation.
## Requirements
- Docker
- Python3
## Quickstart
First of all, clone the project repository:
    *git clone https://github.com/iByrs/TapBall.git
    cd tapball*
starting out the application is really easy. 
There are two files inside the directory:
- build.sh: 
   + let you build the docker image of the application (you need to do it only the first time).
- docker-compose.yml      
   + let you run the application.
   + ![alt text](https://github.com/iByrs/TapBall/blob/master/docs/img/let-me-know-when-youre-ready-ill-just-be-waiting-here.jpg)
## Note to read before running the application:
There are small steps you must do before running the application:
1) Choose the match:
- Insert into python scripts (/API-Football), your api key. 
- inside the /dataset folder there is the a file called 'Fixture.json', from which you need to choose the l'ID of the match of your preference and then include it inside the python file = 'getMatchStatistics.py'
For more information please visit the website: [link](https://api-sports.io/documentation/football/v3#section/Introduction)

- Inside the /Dataset directory there are simulated real time match from which I requested API the data every five minute. So, in this way it is possible to emulate the API response and the matches.
2) Elasticsearch memory problem:
- It is possible to edit che maximum storage taken up by Elasticsearch by going inside the docker-compose.yml and then in the Elasticsearch section and edit these parameters: 
   + discovery.type=single-node 
   + ES_JAVA_OPTS=-Xms%dg -Xmx%dg
   + where %d = the edit number of RAM

3) Decision Tree
- In the project there are four decisional trees, you can choose the one you prefer by going to 'main.py' file, from there  you need to change the directory with the directory of the decisional tree of your preference
   + ![alt text](https://github.com/iByrs/TapBall/blob/master/docs/img/Tree.png)

# THAT'S ALL!

## Data visualization 
To view the chart of the received data, go to localhost:5601 and choose 'tapball' as index

