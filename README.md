# Book Review Website

Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. A third-party API by Goodreads, another book review website,is used to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via website’s API.

### Prerequisites
all requirments exist in requirements.txt

* run the following command
```
pip3 install -r requirements.txt
```

* you need to export the URI of your database
```
export DATABASE_URL=The URI OF YOUR DATA BASE
```
* run import.py to insert the data inside books.csv into your database,
```
python import.py
```
wait until data is uploaded to your database


