# PR TRACKER

#### Video demo: https://www.youtube.com/watch?v=PSEs7yLWNes&ab_channel=jasonchan

#### Description:

##### Hello, I have created a web application which tracks your personal records in the gym, namely for the 3 more important exercises, the squat, bench and deadlift. As I personally go to the gym, this was something that I thought would be a good record of progress. I used python Flask, javascript, html and css to design the application.

##### The index page is relatively simple. Before logging in there is a navbar with the logo on the top left which when clicked leads to the index, and the buttons for registration and login on the top right. Registration is simple entering a username along with a password and a confirmation. The visibility of your password can be toggled in order to make sure that you have not made any mistakes. Once you have registered you are redirected to the login page. After logging in, flask takes a note of the current session using a user_id assigned during registration.

##### Once a user _id is logged, the index page changes to show a PR tab and a log out tab. If you are newly registered the main part of the index page should be empty, with only a greeting based off of your username.

##### Clicking into the PR section you are prompted with a form to input the exercise, weight and date at which you achieved a new personal record. Once submitted, a table should appear showing the weight and the date of the input along with the associated exercise. As you input more weights, the table will accordingly build up. Above each of the tables should also show the highest weight that you have lifted as well as the date at which you performed this feat. Additionally you are also free to delete any inputs in case you may have accidentally pressed the button or entered a incorrect result.

##### Then returning to the index page. The layout will have changed if there have been inputs in the exercises. There should a circular division for each of the lifts highlighting your current personal best, your most recent entry into the application of the certain exercise as well as the percentage improvement that you have made to each lift according to your first input. Below these values should also be a sentence with a link which will redirect the user to an instructive video on the proper form that should be executed when performing any one of these exercises.

##### There is also a apology.html which is rendered whenever a user inputs something incorrect into any forms, displaying a message to guide the user to fix their input mistake.

##### Finally, the logout button clears the current flask session and returns the user to the login page. Aside from the login and registration page, the other actions contain decorater functions which check that the application currently has a user session to ensure that users who have not logged in cannot access these pages. This function is stored in the helper.py file.

##### In terms of storing the user and exercise data an sqlite database named "track.db" was created. In it there are 4 tables. One for the user data(user_id, username and password) which is logged whenever someone completes the registration form. This checks for identical usernames, and assigns each new user with a unique id. Then for each of the exercises a separate table is created, recording the user_id, weight and the date entered. These values are queried throughout the application in order to display them.

##### In app.py get and post methods are used to signal whenver a form is being submitted and perform an action related to it. Mainly in the registration and logging of a new PR. Aside from that sqlite is used to query the database and return meaningful data to display.