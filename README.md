# Discord Study Bot

## Project Purpose
The inspiration for this project was my wife and her request for a digital study-buddy to help her with exam prep while in grad school. 
After discussing several options, we decided that the simplest solution was to run a webserver on a raspberry pi that could remotely send study questions to a discord channel. 
At the time of writing, there are 40+ students subscribed to the channel and using the study bot to help them with exam prep.

With the current configuration, the server will select a random question from the eligible datasets for each channel and post it every two hours between 8am and 8pm EST.
By using the custom formatting that discord has made available, we are able to post the questions with the answers blacked out (similar to spoilers on Reddit for those who are familiar) and once the student believes they know the answer, they can click on the blacked out text to see if they were correct.

## Data Source
The source of the study material are series of flashcards that my wife created on a webiste called Quizlet. We are able to export these flashcard sets and use them as the basis for our application.

## Other Requirements
Project Assumptions:
 - You have configured your local database (in this case we are just using MySQL)
 - A discord channel has been setup and webhooks have been generated

## Project Setup and Configuration
Please see the SETUP.txt file in this project for more details on how to setup the project and run the server
