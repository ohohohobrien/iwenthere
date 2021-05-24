# I Went Here

This is a web application developed with the Django framework to be mobile responsive.

This is designed with the idea to allow users to easily share their local area's hidden gems. 

This allows the user to interact with a map and plot a path and provide points of interest, then provide further details and images to share with other users.

If the user wants to find somewhere nice in their local area, they can instead search through a list of walks.

## Access

This can be accessed via the following link [I Went Here](https://ohohohobrien.pythonanywhere.com/).

This is hosted here for testing purposes. If the project were to scale, a better solution would be required.

## Usage

The website has the following features:

* Search

    This allows the user to search a country then state and additionally the category of walk they would like. The user is then redirected to the results of their search. If a match was not found, they will be prompted to create one.
    
    This utilises Javascript to make a fetch request upon update of the "Country Name" dropdown list to fetch the relevant "State Name" list. Once ready, this form is sent as a GET request to Django and provides a list of user made maps that were obtained from a query of the database. These are then pagified to show 10 at a time.

* Display Map

    The user can then click on one of the results and is taken to a map screen that provides details of the walk such as: 

    1. Interactable map with inbuilt GPS tracking
    2. Titles, descriptions, distance, duration, starting location and images
    3. If this is the user's created map, they can edit or delete the entry.

    In addition to this, the map primary keys are hashed to make the database more secure.

* Login

    In order to share a map, the website requires an account. To make this simple and secure, I have implemented Google accounts as a social account feature of Django instead of creating these myself. A profile page is then also generated at ""/USERNAME" for the user.

* Create

     When a user wants to share a map, they are presented with an interactable map which they can draw upon to provide to other users. 
     
     The map is making use of OpenLayers v6. When submit is clicked, the JS will save the geoJSON data that was input to a secret form field to submit to the server.
     
     When the form is submitted to Django, the server will automatically calculate the distance, where the map should open to (regex to initial coordinates in the geoJSON) and provide numbered points for each map interaction.
     
 * Profile Page

    Here users can see the list of maps that a user has created at "/USERNAME". 
    
    When a user clicks onto a map they created, they can see an edit and delete button for that map.

# Additional Details

This was built as a passion project to allow people to share local areas to explore. With recent events, travel has become more and more difficult, but if there were nice areas to explore in your local area, maybe travel could once more become a little more possible.

There are many more features I would like to implement such as:

* better editing of maps (especially map interaction in OpenLayers)
* allowing users to provide information for each point placed 
* allowing users to click on points to access that information
* commenting
* likes
* following
* saving maps

But for now, I am happy with the project so I will leave it here for now.
