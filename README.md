# Mission-to-Mars

This project consists of web-scraping functions to gather news regarding the mars exploration and the relevant images.

## Overview

The web app is based on flask using html elements to give a better presentation to the scraped information. All of the scraped data is stored in a Mongo database in which the newer entries are written.

The web app has 2 endpoints; the index which is the landing page and shows the scraped data, and the scrape endpoint which goes through different websites to obtain new information.

### Responsiveness

This web app is responsive to different display sizes as shown in the following examples:

#### Desktop View

!["Desktop"](/images/web_app_desktop_view.png)

#### Samsung Galaxy View

!["Galaxy_A51"](/images/web_app_samsung_galaxy_a51_view.png)

#### Ipad Mini View

!["Ipad_Mini](/images/web_app_ipad_mini_view.png)

This is done by using the bootstrap img-responsive class on the images.

### Table

The table has the bootstrap table-bordered, table-striped and table-hover classes in it by including them in the pandas DataFrame.to_html function as seen in the following code line:

~~~~
return df.to_html(index = False, bold_rows = False, classes=["table-bordered", "table-striped", "table-hover"])
~~~~

This ensures that the returned table in html format already includes the appropriate classes.

### Hemisphere images

The hemisphere images shown in the Desktop, Samsung and Ipad Mini views are included as thumbnails in the final row of the web app. These images work as a hyperlink to the full url from where they were scraped by clicking or touching them depending on the device.

~~~~
<a href="{{hemisphere.img_url}}"><img src="{{hemisphere.img_url | default('static/images/error.png', true)}}" class="img-responsive img-thumbnail"></a>
~~~~

### Scraping functions

The data obtained from the different scraping functions called by scrape_all is stored in the data dictionary and stored in Mongo. Then it's retrieved through app.py to be shown in the flask web app.

~~~~
data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now(),
    "hemispheres" : hemisphere_images(browser)
}
~~~~

A brief overview of each function will be given below.

#### News Title and News Paragraph

This function parses the website using beatiful soup and the html parser and then looks for the div class list_text which contains the article's date, header and the teaser information. 

The function extracts the content_title and article_teaser from the latest news.

#### Featured Image

This function uses the browser to look for the Full Image button (which is the second instance of the button class in the website) and clicks on it to open the image. The new website is then parsed using beautiful soup and retriveves the relative url which is then joined with the website's url.

#### Facts

This function converts the first table in the website into a pandas DataFrame using the read_html() function and then exports it with the necessary html using Pandas to_html().

#### Hemispheres

The hemisphere images are retrieved from the website by parsing it and looking for all anchor elements with the itemLink class. Then, using a for loop, the relative urls from the parsed html website are joined with the website's url if the href from the anchor contains the extension .html and appended into a list. This list with the full urls is then cleaned from any duplicate entry.

After the url list is clean and ready to use, a for loop is used to make the browser visit each of these addresses to find the full-size download link as well as the image's title and they're both stored in a dictionary.

## Results

The scrape_all function retrieves the latest news and featured image from the requested websites. This flask web app will continue updating as long as the user clicks on the scrape all button. Thanks to the bootstrap elements, this web app is visible on different devices.