import webbrowser

global dataAsList

dataAsList = [['country','Female labor participation rate']]

# Code to start from for HW12, Fall 12, question 2
#
# This problem asks you to use
#  1) use web API calls to retrieve data from the World Bank (or similar public data
#     source, if you let me know about it ahead of time)
#  2) display that data using Google Chart Tools
#


#####################################################
# Sample code to retrieve data from the World Bank
#

from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus, quote   
import json

# This function retrieves life expectancy at birth (SP.DYN.LE00.IN)
# for three countries (USA, Brazil, Afghanistan) for the years
# 2000 and 2001
#
# It constructs this URL:
# http://api.worldbank.org/countries/usa%3Bbra%3Bafg/indicators/SP.DYN.LE00.IN?date=2000%3A2001&format=json
# You can copy/paste the above URL into a browser address bar and see the results there.
# They are reasonably readable.


def queryworldbank():
    global results

    # Construct data retrieval URL
    urlbase = "http://api.worldbank.org/countries/"
    countries = quote_plus("usa;bra;afg;chn;ind;zaf;mdg;dom;fra;gha;idn;ita;pak")
    query = "/indicators/SL.TLF.CACT.FE.ZS?"
    args = urlencode({'format': "json",
                      'date': "2010:2010",
                      'per_page' : 100})
    url = urlbase+countries+query+args
    #print('url',url)

    # Retrieve the data.  The World Bank returns it in 'json' format.
    # json.loads processes the result and we store it in jsonresult.
    # jsonresult is a two-item list.  The first item is a dictionary
    # with information about how many "pages" of results exist.  Only
    # the first page of results is immediately returned.  If you need more
    # than one page, you'll have to request later pages.
    # I've set it up so that a page can contain 100 results, so as long
    # as you don't request a lot of data, you can ignore this first item
    # and just use the second one (see below).
    #
    # The second item is a list of results.  
    
    wbresult = urlopen(url).read()
    wbresult = wbresult.decode('utf-8')
    jsonresult = json.loads(wbresult)
    pageinfo = jsonresult[0]
    print("The World Bank query yielded {} results on {} page(s)".format(pageinfo['total'], pageinfo['pages']))
    results = jsonresult[1]

    # Each of the items in results is a dictionary containing some of
    # the data you requested.
    # You should examine one of the results in the list returned below to
    # determine what fields you need to extract from it.
    # For example, here is one of the six results for the life expectancy
    # query:
    #{'date': '2001', 'country': {'id': 'AF', 'value': 'Afghanistan'}, 'indicator': {'id': 'SP.DYN.LE00.IN', 'value': 'Life expectancy at birth, total (years)'}, 'decimal': '0', 'value': '45.5672682926829'}
    #
    #print(results)
    return(results)
    
    


#####################################################

# Sample code for "hack-y" way of using Python to create web pages
# displaying Google Charts.
#
# The standard way to create Google Charts is to write Javascript (another
# language, like Python) and incorporate that directly into a web page's
# HTML source code.
#
# We haven't covered Javascript in this class, so we're going to "hack it"
# by starting from some HTML/Javascript that Google provides, and modify it
# via Python.
#

# In this example, we re-create the example from Google's Geo Chart page:
# https://google-developers.appspot.com/chart/interactive/docs/gallery/geochart
#
# We construct a big string that is HTML and Javascript.  You don't really
# need to understand much of the code.  You're just going to fill in *data*
# (created from your World Bank query) in the right part of the big string.
#
# I broke the HTML/Javascript into two basic parts -
#    a) geochartHTMLpart1 - the code *before* the chart data
#    b) geochartHTMLpart3 - the code *after* the chart data
#
# To make a working Geo Chart web page, you simply need to make one big string
# combining part1 , a string for the data, and part 3.
# writeGeoChartHTML does that.
# 
# This example allows a tiny bit of customization over the Google example.
# The writeGeoChartHTML() function takes a country name and value
# as arguments, so that the resulting web page has one more country filled
# in than in the original data.
#
# To run the example, do:
#   1) writeGeoChartHTML("Peru", 1000)
#        (or any other country and value)
#   2) showwebfile("geochart.html")
#
# Note: you need to change the urlbase variable below so that the browser
# properly finds your generated html file.

geochartHTMLpart1 = '''<html>
<head>
  <script type='text/javascript' src='https://www.google.com/jsapi'></script>
  <script type='text/javascript'>
   google.load('visualization', '1', {'packages': ['geomap']});
   google.setOnLoadCallback(drawMap);

    function drawMap() {
      var data = google.visualization.arrayToDataTable(
    '''

geocharHTMLpart3 = '''
        );

      var options = {};
      options['dataMode'] = 'regions';

      var container = document.getElementById('map_canvas');
      var geomap = new google.visualization.GeoMap(container);
      geomap.draw(data, options);
  };
  </script>
</head>

<body>
  <div id='map_canvas'></div>
</body>

</html>'''

def createData(additionalCountry, value):
    global dataAsList
    dataAsList.append([additionalCountry,value])
    #print(dataAsList)
    
    return(str(dataAsList))
          
def writeGeoChartHTML():
    global results
    global valueList
    global countryID
    global dataAsList
    of = open("geochart.html", 'w')

    dataList = []
    dataString1 = ''

    for i in range(len(results)):
        createData(countryID[i], valueList[i])
    #print(dataList)
    #print(dataString1)
    html = geochartHTMLpart1 + str(dataAsList) + geocharHTMLpart3
    #print(html)
    of.write(html)
    of.close()

def MakeChart():
    global results
    global valueList 
    global countryID
    valueList = []
    countryID = []
    queryworldbank()
    for i in range(len(results)):
        tempResult = results[i]
        valueList.append(tempResult['value'])
    #print(valueList)
    for i in range(len(results)):
        tempResult2 = results[i]
        tempResult3 = tempResult2['country']
        finalTempResult = tempResult3['id']
        countryID.append(finalTempResult)
    writeGeoChartHTML()
    showwebfile('geochart.html')
    
   
    


# NOTE: You must change the value below!
urlbase = "file:///Users/imason/Desktop/hw12f12data/attempt1/"

# E.g. showwebfile("geochart2.html")
def showwebfile(filename):
    webbrowser.open(urlbase + filename)








