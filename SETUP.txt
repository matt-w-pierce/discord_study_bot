--- This is an introduction and running instructions ---

--- Installation and Setup ---
1. Cloe the repository onto local machine
2. Create virtualenvironment and install all python dependencies using the requirements.txt
3. Make sure all dependencies have been installed and project has been updated 

--- Running the server ---
1. Make sure flask is pointing at the correct application script: export FLASK_APP=application.py (on Windows: set FLASK_APP=application.py)
2. Run the following command in the base directory: flask run
3. You should then see that the application is running on localhost

--- Adding new question sets ---


--- Adjusting Discord Message Parameters --- 
All discord message parameters are set in discord_study_bot/app/main/post_question.py
There are a set of scheduled tasks in the format "@scheduler.task(trigger='cron', id='...', hour='...', args=[])"
The arguments passed to this scheduler task are determine how discord messages are sent

		-- Message Frequency --
	The "hour" argument in the scheduler task dictates how frequently messages are sent
	Current default (2021-10-31) is "8-20/2" which will send messages from 8am to 8pm, every 2 hours on the hour
	There are a whole bunch of different options for message frequency

	-- Adding/Removing Classes -- 
	Each scheduler task has been configured for a different class/subject
	Adding or removing scheduler tasks will change which subjects/classes are active

	-- Adding/Removing Subjects --
	Within each class there can be multiple subjects (e.g. Math --> Geomerty, Algebra, etc.)
	The "args" argument sets the list of subjects within the class
	"args" is expecting 3 arguments to be passed as a list, the first is the list of subjects. 
	Adding or removing items from this list will add or remove subjects. If there is a probability balancing for the class make sure to adjust accordingly (see below)

	-- Adjusting Message Subject Probability --
	For each class, the probability of any given subject being chosen can be set. 
	This can help skew questions towards current exams while allowing for previous subjects to be included
	Subject frequency is passed as an element of the "args" argument. The first element of the "args" list is the subject list, the second is the weight list
	If you want to set weights then a list should be passed with weights that is equal to the length of the subject list
	If weights are not needed then a question will be chosen randomly from that class without considering the subject, just pass None as the argument

















