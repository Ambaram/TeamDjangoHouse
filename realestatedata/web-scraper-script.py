class WebScraper():
    def p2hScrape():

        '''
        WEB SCRAPER FOR POINT2HOMES.COM

        Pulling new listings for all six major Metropolitan areas
            Toronto
            Montreal
            Vancouver 
            Calgary
            Edmonton
            Victoria
        '''

        from urllib.request import urlopen, Request
        from bs4 import BeautifulSoup
        from datetime import date
        import re
        '''
        import mysql.connector

        # div class holding each item: class="item-cnt clearfix" (id = unique id per listing)
        # address = div class="address-container" (text or data-address)
        # beds = li data-label="Beds"
        # property type = class="property-type ic-proptype
        # price = div class="price " data-price="$1,199,000 CAD" (will need to sort out price with regex, conv to integer)
        '''
        headers = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        for i in range(0,20,1):

            url = 'https://www.point2homes.com/CA/Real-Estate-Listings.html?location=Toronto%2C+ON&search_mode=location&page={}&sort_by=DESC_listing_created&SelectedView=listings&LocationGeoId=783094&location_changed=&ajax=1'.format(i)

            req = Request(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'})

            html = urlopen(req)
            soup = BeautifulSoup(html.read(), 'html.parser')

            listing = soup.findAll('div', 'item-right-cnt')
            i = 0

            for item in listing:
                try: 
                    address = item.find('div',"address-container").text
                    price = item.find("div", "price").get_text()
                    

                    beds = str(item.find("li", "ic-beds"))
                    
                    linkUrl = str(item.find("a", "btn-secondary btn-lg"))
                    linkSplit1 = linkUrl.split('href="')
                    linkSplit2 = (str(linkSplit1[1])).split('" onclick')
                    linkFinal = "http://point2homes.com" + linkSplit2[0]

                    beds = beds.split('<strong>', 1)
                    bedSplit = beds[1].split('</strong>', 1)

                    bedFinal = int(bedSplit[0])
                    i = i + 1

                    #clean address string
                    address2 = re.sub(' +', ' ', address)
                    address3 = address2.split("  ", 1)
                    address = address3[0].strip()
                    postalsplit = address.split('Ontario ', 1)
                    postalcode = postalsplit[1]





                    price = re.sub(' +', ' ', price)
                    price = price.strip()


                    #set values
                    date = date.today()
                    city = "Toronto"

                    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
                    print("Entry #" + str(i), "\n", date , "\nBeds: ", bedSplit[0], address, price)
                    #figure out urllink to print clean
                    print(linkFinal)
                    print(postalcode)

                    ''' INSERT LISTING INTO DB'''
                    ######      BEGIN INSERT DATA INTO DATABASE     #####

                    import mysql.connector
                    import re

                    #DB information to connect to localhost

                    mydb = mysql.connector.connect(
                    host="localhost",
                    port="3306",
                    user="root",
                    password="root",
                    database ="realestatelistings"
                    )

                    #get everything from the listing table

                    mycursor = mydb.cursor()

                    try:
                        print('listing does not exist in record. Creating new Listing ID:')
                        sqlListing = "INSERT INTO listings (address, price, city, bedrooms, scrapedate, postalcode) VALUES (%s, %s, %s, %s, %s, %s)"
                        valListing = (address, price, city, bedFinal, date, postalcode)

                        mycursor.execute(sqlListing, valListing)
                        print("Adding to database: ", address, ": ", price)
                        mydb.commit()
                    except: 
                        print('unable to add to db')
                        pass


                except: 
                    pass
                    print('error pulling listings in webscrape.')
    p2hScrape()