# CS50W Food Tracker

**CS50W Food Tracker** is a web application implemented using **Python**, **JavaScript**, **HTML**, and **CSS**, that allows users to track their food consumption, count calories and macronutrients in their diet, and monitor their weight. 

## Getting Started

1. Download the submitted code.
2. In your terminal, `cd` into the `foodtracker` directory.
3. Run `pip install -r requirements.txt` to install the necessary dependencies.
4. Run `python manage.py makemigrations foodtracker` to make migrations for the `foodtracker` app.
5. Run `python manage.py migrate` to apply migrations to your database.
6. Run `python manage.py runserver` to start the server.
7. Once the server is running, you can access the application by navigating to http://127.0.0.1:8000/ on your local web browser.

## Specification

* **Food List**: This is the default route that lists all foods available in the application. 
    * The Food List page is available to all users of the application.
* **Pagination (Food List page)**: For the users' convenience, the list of all food items available in the application is split into separate pages. 
    * Four food items are displayed on each page.
* **Food Details**: Clicking on the 'View details' link of selected food takes the signed-in user to a page specific to that food item. 
    * On that page, the user can view all information on the food, including the number of calories per 100 grams and the macronutrients breakdown (the amount of fat, carbohydrates, and protein in 100 grams of food). 
    * A horizontal bar chart displayed on the food details page helps the users visualize the macronutrients breakdown of the selected food.
* **Food Categories**: The list of all food categories is displayed in the sidebar.
    * Clicking on the name of a food category takes the user to a page that shows all of the foods in that category. 
    * The user needs to be signed in to access the list of foods in each food category.
* **Add Food Item**: The signed-in user can add new food that can be later used by the user in their food log. 
    * The user must specify a food name, food category, quantity (the default is 100 grams), the number of calories, fat, carbohydrates, and protein per the specified food quantity. 
    * The user can also add up to two images of the new food item.
* **New Food Item Added to the Food List**: The new food added by the user is displayed on the Food List in the application. 
* **Food Log**: Signed-in users get access to the Food Log page, which allows them to track details of their food consumption. 
    * Users can add and remove foods from their Food Log. 
    * An animated progress bar indicates the user's progress towards their daily calorie goal as they add new foods to their food log. 
    * A doughnut chart displayed on the food log page helps the users to visualize the macronutrients breakdown of all the foods in the food log so that the user can better track their results. 
    * The doughnut chart and progress bar reflect the values from the last row of the food log (Total).
    * The progress bar tracks the total calories value, and the doughnut chart tracks the total fat, total carbohydrate, and total protein values.
* **Add Food to the Food Log**: On the Food Log page, signed-in users can add new foods to their Food Log.
* **Remove Food Item from the Food Log**: Signed-in users can remove foods from their Food Log.
* **User Profile**: Users who are signed in can visit a User Profile page, which displays various data associated with the user. 
    * Each user gets access to a weight log so that they can record their weight at different points in time. 
    * Users can add and remove records from the Weight Log. 
    * An area chart displayed on the user profile page helps users visualize their weight history and better track their results.
* **Record Your Weight**: On the User Profile page, signed-in users can add records to the Weight Log (their weight in kilograms and a date when the measurement was made).
* **Delete record from the Weight Log**: Signed-in users can remove records from their Weight Log.
* **Django Admin Interface**: Via the Django admin interface, a site administrator can view, add, edit, and delete any users, foods, food categories, food images, and food log, and weight log data recorded in the application. 
* **Responsive Web Design**: The application renders well on a variety of devices and screen sizes.

## Distinctiveness and Complexity

I believe that CS50W Food Tracker is sufficiently distinct from the other projects in this course and more complex than the previous projects that I have already completed.

CS50W Food Tracker utilizes **Django** on the back-end and **JavaScript**, **HTML**, and **CSS** on the front-end.

CS50W Food Tracker allows users to track their food consumption, count calories and macronutrients in their diet, and monitor their weight. One of the main components of this application that makes it unique and distinct from the other projects in this course is a variety of **visualization tools** written in **JavaScript** (using **Chart.js** and **jQuery** JavaScript libraries). These visualization tools help the users of the application to organize and clarify their data and better track their progress to help them achieve their nutrition goals.

Visualization tools in the CS50W Food Tracker include:

#### Area Chart

![plot](/foodtracker/static/foodtracker/images/weight_history.png)

An area chart displayed on the User Profile page helps users visualize their weight history and better track their results. The chart is updated dynamically in JavaScript as users add and remove records from their Weight Log.<br />
For details, see file: `foodtracker/static/foodtracker/js/userProfile.js`

#### Doughnut Chart

![plot](/foodtracker/static/foodtracker/images/macronutrients_breakdown_doughnut.png)

A doughnut chart displayed on the Food Log page shows the macronutrients breakdown of all the foods consumed by the user and registered in their Food Log (the total fat, carbohydrate, and protein values). The total values are dynamically calculated in JavaScript as users add and delete new foods from their Food Log.<br />
For details, see file: `foodtracker/static/foodtracker/js/foodLog.js`

#### Calorie Goal Progress Bar

![plot](/foodtracker/static/foodtracker/images/progress_bar.png)

An animated progress bar displayed on the Food Log page indicates the user's progress towards their daily calorie goal. The total calories value is dynamically calculated in JavaScript as users add and delete new foods from their Food Log.<br />
For details, see file: `foodtracker/static/foodtracker/js/foodLog.js`

#### Horizontal Bar Chart

![plot](/foodtracker/static/foodtracker/images/macronutrients_breakdown_bar.png)

A horizontal bar chart displayed on the Food Details page shows the macronutrients breakdown of each food available in the applications.<br />
For details, see file: `foodtracker/static/foodtracker/js/foodDetails.js`


Another characteristic of CS50W Food Tracker is its **responsive design** - the application renders well on a variety of devices and screen sizes due to the use of **Bootstrap**, which is a CSS framework directed at responsive, mobile-first front-end web development. All visualization tools in the application are responsive as well.

CS50W Food Tracker utilizes **Django** on the back-end and uses **six models**:
* `User`
* `Food`
* `FoodCategory`
* `FoodLog`
* `Weight`
* `Image`

For details, see file: `foodtracker/models.py`

The application also utilizes **Django Forms**.<br />
For details, see file: `foodtracker/forms.py`

## Understanding

In the submitted code is a **Django** project called `config` that contains a single app called `foodtracker`.

#### The `foodtracker/urls.py` file

The URL configuration for this app is defined in the `foodtracker/urls.py` file. The routes defined in this file are the following:
* a default `index` route, 
* `/login`
* `/logout`
* `/register`
* `/profile/weight`
* `/profile/weight/delete/<int:weight_id>`
* `/food/list`
* `/food/add`
* `/food/foodlog`
* `/food/foodlog/delete/<int:food_id>`
* `/food/<str:food_id>`
* `/categories`
* `/categories/<str:category_name>`

#### The `foodtracker/views.py` file

The `foodtracker/views.py` file contains the views associated with each of these routes:
* The `index` view renders a list of all food items.
* The `login_view` view renders a login form when a user tries to GET the page. When a user submits the form using the POST request method, the user is authenticated, logged in, and redirected to the index page. 
* The `logout_view` view logs the user out and redirects them to the index page. 
* The `register` view displays a registration form to the user and creates a new user when the form is submitted.
* The `weight_log_view` view renders the user profile page where the user can record their weight.
* The `weight_log_delete` view allows the user to delete a weight record from their weight log.
* The `food_list_view` view renders a page that displays all food items.
* The `food_add_view` view displays a form that allows the user to add a new food item.
* The `food_log_view` view renders the food log page where the user can record their food consumption.
* The `food_log_delete` view allows the user to delete a food record from their food log.
* The `food_details_view` view renders a page that displays the details of a selected food item.
* The `categories_view` view renders a list of all food categories.
* The `category_details_view` view renders a page that displays foods that belong to a selected food category.

#### The `foodtracker/models.py` file

The `foodtracker/models.py` file contains the models for the application, where each model represents some type of data stored in the database. There are six models:
* `User`
* `FoodCategory`
* `Food`
* `Image`
* `FoodLog`
* `Weight`

to represent details about users, foods, food categories, the food log, and the weight log.

####  The `foodtracker/forms.py` file

The `foodtracker/forms.py` file contains Django Forms logic to generate forms for adding a new food item and adding food images to the food items.

#### The `foodtracker/templates/foodtracker/` directory

The `foodtracker/templates/foodtracker/` directory contains all of the Django templates used in the application. Django templates consist of the static parts of the desired HTML output as well as the parts created using the **Django template language** (**DTL**) describing how dynamic content will be inserted.

#### JavaScript files

The `foodtracker/static/foodtracker/js` directory contains JavaScript files:
* `userProfile.js`
* `foodLog.js`
* `foodDetails.js`

These files contain the code of a variety of **visualization tools** written in **JavaScript** (using **Chart.js** and **jQuery** JavaScript libraries). These visualization tools help the users of the application to organize and clarify their data and better track their progress to help them achieve their nutrition goals.
