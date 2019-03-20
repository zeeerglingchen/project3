In this program, I set up 4 tables to store data, which are movie table, genre table, director table and MPAA rating table.
The relationships between moive table and director table, moive table and genre table, moive table and MPAA rating table are all many-to-one type, so the movie tables contain three foreignkeysw within it.
Then I wrote codes to transfer the data from previous csv file to the database, which I thought is one of the requirements of this project. It will store the csv data in a database called "movies.dbx"
The first route will display how many data records exist in the current database
The second route enables users to insert data by inputing value in the web browser and adds the data into the database
The third route queries the rating table and display all kinds of raing types on the screen
In order to run this program, you will just need to type "python SI507_project3" in the terminal
