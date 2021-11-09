# Disclaimer

* I do not promote, encourage, support or excite any illegal activity or hacking without written permission in general. The repo and author of the repo is no way responsible for any misuse of the information.

* "spotify_scraper" is just a terms that represents the name of the repo and is not a repo that provides any illegal information.

* The Software's and Scripts provided by the repo should only be used for **_EDUCATIONAL PURPOSES ONLY_**. The repo or the author can not be held responsible for the misuse of them by the users.

* I am not responsible for any direct or indirect damage caused due to the usage of the code provided on this site. All the information provided on this repo are for educational purposes only.



## Usage

1. Go to the https://spotifycharts.com/regional/us/daily/ and extract the raw headers from the request. One of the headers will be labeled 'cookie'. Take this long string and set the variable 'COOKIE' in the beginning of the script to this value.

2. Modify start_date and end_date variable according to preference.

3. Run the request_spotify() function to generate an Excel file containing all top song (track & artist, streams, and date) data from start_date to end_date.

4. To create a bar chart race HTML file using the data you just scraped, run the code below the function call request_spotify().

5. Convert the HTML file to video with the image_to_video.py script

