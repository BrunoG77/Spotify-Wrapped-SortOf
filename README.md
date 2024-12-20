# Get Spotify Wrapped whenever you want!
#### Description:
For my final CS50 project, I decided to make a website that makes and stores the famous ***Spotify Wrapped*** information of the user, this being the users **top artists** and **top tracks** during any time of the year, in which the user has to create an account and log in. 

These were the things I had in mind to do
- Make the project using ***Python***
- Use ***Flask*** to create a website
- Create the routes needed
- Use *render_template* to render html files to personalize the page
- Utilize ***SQL*** to create database with the user info
- Use *login_manager* to keep user logged in
- Create an app on the *Spotify web developer app*
- Use *Spotipy* to connect with the ***Spotify API*** and get permission from my app
- With *spotipy*, get the users top artists and tracks
- On the home page, store users ***Spotify Wrapped*** information, so the person can access it at any time and see how the music taste is changing over the years
  
#### Decision making
This wasn't that hard. I decided to use *Python* since it was the language I had the most fun with and has a library called *Spotipy* that would facilitate the project I had in mind.

I wanted to create something interactive with possible real life use. With this in mind, I would need to use a framework, either *Flask* or *Django* to make the web application. Decided to go with *Flask* since it's the most simple of the two.

In this, I also had in mind the creation and deletion of user accounts, of *Spotify Wrappeds* and the managing of a theoretical web server, so I knew I had to use *SQL* to manage the database.

The objective was to have the *home page* serve as a history of *Spotify Wrappeds*, so the user could see how its taste had change over the years and a *Wrapped page* to calculate the actual *Spotify Wrapped* of that instant. The *Spotify API* can give me a short term (1 month), medium term (6 months) or long term (years) of data which could make this even more fun.

### Code
The main file is `main.py` and it's the one to execute so the app works.

| Code         | Description                         |
| ------------ | ----------------------------------- |
| create_app() | Function imported from the website folder that sets up and initializes the app |
| app.run(debug=True) | Let's me debug and see errors on the web page |

The *`.flaskenv`* is so the flask environment is obliged to be `main.py`.

The ***website*** folder is a Python directory that stores all the code for the website. It has the `__init__.py` file which tells Python that the website folder is a *Python package*, so I can import anything iside the folder and `__init__.py` will run automatically.

#### Inside website
Inside the *website* folder, I have the *static* folder, which contains static content like *JavaScript* and *CSS* files used in the project. 

| File         | Description                         |
| ------------ | ----------------------------------- |
| index.js | Contains an on-click function to delete data from the database |
| style.css | Personalizes table content for the html used in the home page |

And inside the *templates* folder, I have the *html* templates for the website. These are the front-end of the project.

| File          | Description                         |
| ------------- | ----------------------------------- |
| `base.html`     | This is the base html file, which has the base content that I want for every other html file, so it has a block container so every other html file can extend over the base content. Has the flash messages coded here and a button to close the messages. With *Django* has an if statement that checks if the user is logged in, via *flask-login*, shows the home, redirect, wrapped and logout tabs if indeed logged in and the login and signup tabs if not. |
| `home.html`     | It extends from the base file. This template does the history of the *Spotify Wrapped* of the user in a table. The *Date* header lists the date of when the user did their *Spotify Wrapped*. The *Wrapped type* lists what type was that specific *Spotify Wrapped*, was it short, medium or long term. The *Artists* header lists the *Top 5* artists of the asked term. The *Tracks* header lists the *Top 5* tracks. The *Delete Wrapped* header has a button to close and delete the row from the history table and the database. For the rows, a *for* loop is going through the database of said user and displaying the *Spotify Wrappeds*. The button has an on click function, that is coded in the index.js file and routed to the *`delete-wrapped`* function in `home.py`. |
| `login.html`    | It extends from the base file. Has a *post method* form, so the user can input his email and password and a submit button with a post request, so the server can analyse the information on `auth.py`, to see if the user has an account and the password is correct in order to log in. |
| `redirect.html` | It extends from the base file. Simply has text saying that *Spotify* has accepted the user. |
| `signup.html`   | It extends from the base file. Similar to `login.html`, it has a *post method* form, with inputs for the email address, first name, password, the confirmation of the password and a button to submit so the information is handled on a post request in `auth.py`. |
| `wrapped.html`  | It extends from the base file. Also has a has a *post method* form, but this time only with 3 buttons. Short, medium and long term buttons, when the user hovers over the said button, it displays how long the term is for. When clicked, `wrapped.py` will use the post request information and send the top 5 artists and tracks in variables so they can be displayed on the wrapped page. |


#### Back-end

For the back-end there are several python files that do the actual work and also `database.db`, the database file created with *SQL* that contains the data about the user.


#### `__init__.py`

This file is ran automatically and is the one that initializes the app. Down below is a table with the functions explained.

| Functions                |      Description          |
| ------------------------ | -----------------------   |
| `create_app()`           | This function initializes the app by configurating the web session, like setting the session secret key, so *Flask-Login* can work and initiating the database. It registers the blueprints, so every file and route are connected when executing the app. Then it creates the database. The login manager contains the code that lets the application and *Flask-Login* work together, such as how to load a user from an ID, where to send users when they need to log in, etc. So I define *login manager*, this to force the user to the login page if not logged in and associates the login with the app, it knows if the user is logged in or not. When logged in, it tries to get the id of the user. |
| `load_user(id)`          | This function is inside a decorator for `@login_manager.user_loader`, because it is needed to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object. It should return None if the ID is not valid. |
| `create_database(app)`   | This creates the database file if not yet created.Its checks to see if a `database.db` was yet created in the specified path, if not it creates it there. |
| `create_spotify_oauth()` | This function uses the `SpotifyOAuth` library to connect with the *Spotify API* and the app that I created there. It takes the *client ID*, the *client secret* of the *Spotify* app, the *redirect URI* to redirect the user to the specified page so *Spotify* can ask if the user lets the web application get data from their *Spotify* account and the *scope* to specify what the scope of search is. In this case it's `user-top-read` so `SpotifyOAuth` can get the top 5 artists and tracks. |
| `get_token()`            | This function starts by getting the session token, if it's none throw an exception, because the session needs a token. If it has one, check how long it has left and if it's less than an hour, it refreshes the token. |


#### `auth.py`

This file has the functionalities related to authorization, gets *Post requests* from the server to analyze, makes sure the password is stored safely by hashing it with *sha256*, stores the data in the database and logs in the user.

| Funtion         | Description                           |
| --------------- | ------------------------------------- |
| `sign_up()` | This route can receive a *GET* and a *POST* method request like the other routes in this file. If it does receive a *POST* request, that means that the user has clicked the button and submitted his information. So first I store the info from the email, name and password inputs in variables to analyze. I then check multiple things like the database to see if a user with the same email inputted exists, if the email, name or password have enough characters and if the passwords match, to check if this data is correct and could be stored in the database. If it's all good then I add everything to `database.db`, but I hash the password with *SHA256* so hackers cannot get the users password. Finally I log in the user to *flask* and redirect him to the home page. |
| `login()` | Similarly to `sign_up()`, I check the submitted data with the *POST* request, store the info in a variable, see if a user already exists with that email and also see if the passwords match by hashing the new one and comparing it to the one on the database. If it all matches, log in the user to the home page. If the passwords or email don't match anything, let him try again. |
| `logout()` | Simply logs out the user from flask and redirects them to the login page. |

#### `models.py`

In `models.py` I create and define the schema of the SQL database with *SQL Alchemy*.

| Table         | Description                             |
| ------------- | --------------------------------------- |
| *User* | I define a User class, that will be the User table. It contains the *ID* of the user (the primary key), the email set to unique, so there cannot one equal to another, the password hashed and the name. I create a relationship with *wrapped* utilizing *SQL alchemy* to say that the table *wrapped* will have a foreign key of *User*. |
| *Wrapped* | The *Wrapped* table has an *ID*, a *date* to know when the *Spotify Wrapped* was performed, a *type* to specify what was the term type chosen by the user for the *wrapped*, a user_id to be the foreign key to connect to the *User* table and two relationship connections with the *Artists* and *Tracks* tables. |
| *Artists* | The *Artists* table has an ID, a *short term*, *medium term* and *long term* rows, so every choice has it's own row and *wrapped id* to be the foreign key. |
| *Tracks* | The *Tracks* table is the same as the *Artists* table, except it will store the tracks data. |


#### `home.py`

In `home.py` is where the application talks with *Spotify*, gets access, because in the developer site of *Spotify* I indicated that the redirect URI of my application would be ***http://localhost:5000/redirect/***. It also contains a function to delete the *wrapped* from history in case the user presses the close button on the web app.

| Function      | Description                             |
| ------------- | --------------------------------------- |
| `home_page()` | When in this route, simply render `home.html`. |
| `spot_login()` | This function gets the authorization *URL* of *Spotify*. It's simple, it gets the *URL* of *Spotify* for the authorization process, redirects the user to there, *Spotify* then asks if the user gives permission for the app to use the data, the user clicks agree and *Spotify* redirects the user to the redirect route of the app (the redirect URL was given in the *Spotify* for developers web page and must match the redirect URL of the app). |
| `redirectPage()` | It enters this route when the user agrees to let the app get the `Spotify` data and it redirects it here. First it gets another *Spotify oauth* object, it's needed to have a new one every time we use it. Then the session is cleared to not have any other states, because if we are in this redirected state, we want to clear any other states. Thirdly it gets the authorization code and swaps this with *Spotify* for an access token, so we have granted access to the data and it puts this info on the session. Finally it simply renders the `redirect.html` so the user knows *Spotify* and the application are good and has access. |
| `delete_wrapped()` | This route only  has the *Post* method, because it is only accessed when pressing the close button on the home page. The data received is in *Json*, from `Json.js`, so we load it and put it as a *Python dictionary* in a variable. We get the *wrapped ID* and look for a *wrapped* with the same *ID* in the database. If one exists, then check if it's from the current user. If all checks out, delete *Artists* and *Tracks* from the corresponding *wrapped ID* and finally delete the *wrapped* itself. Return an empty *Json* response, because it wants to receive something in *Json*. |

#### `wrapped.py`

This file does the actual top 5 artists and tracks of the *Spotify Wrapped*. It starts with the *Get* request when the user clicks on this route, it checks to see if this user has the access token in the session. If it isn't there, redirect the user to the login page. With *spotipy* it checks the authorization code of the user given to spotify.
When the user clicks on any of the three buttons on screen, representing the term for the *Spotify Wrapped*, it sends a *Post* request to `wrapped.py` that is picked up. First it sees what term it was and gets the top 5 artists and tracks from that term and stores it into separate variables. This data isn't just the names, it's a lot more information than that. Secondly it checks if there are any artists or tracks on the user top 5, if there are, store in a list only the name of the artists and then the tracks. Thirdly it creates a new *Wrapped*, with the designated term and the user *ID*. Fourthly, depending on the term, it adds the name of the artists and tracks in order and the *wrapped ID* just created. The wrapped table needs to be created first so it can associate the artists and tracks with it after. Finally it prepares the text to show on the web when the user pressed the button and it send the variables and info to *html* to be processed there.

#### Final thoughts

CS50 was a lot of fun and let me create this project that I'm proud of. I'm gonna check my Top 5 monthly to see how my music taste differs and to keep Linkin Park on the number one spot!