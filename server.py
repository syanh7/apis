from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

#ticket master

#zip 94102

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')


    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
                'keyword':keyword,
                'postalCode':postalcode,
                'radius':radius,
                'unit':unit,
                'sort':sort}



    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    #res is a Response object
    res = requests.get(url, params=payload)
    #turn the Response object to a dict object
    data = res.json()
    if data['page']['totalElements'] == 0:
        return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results='')
    #get the events value from the data dict using keys
    events = data['_embedded']['events']

    

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function
    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 'id':id}
     #res is a Response object
    res = requests.get(url, params=payload)
    #turn the Response object to a dict object
    data = res.json()
    #get the events value from the data dict using keys

    events = data['_embedded']['events'][0]

    #gets all image urls
    img_url = events['images'][2]['url']

    #gets the name of event
    event_name = events['name']

    print(events.keys())
    #gets the list of venues from nested events dict
    venues_list = [venue['name'] for venue in events['_embedded']['venues']]


    event_url = events['url']

    classifications = events['classifications'][0]
    classifications_list = []

    for key in classifications.keys():
        if type(classifications[key]) is not bool:
            classifications_list.append(classifications[key]['name'])

    start_date = events['dates']['start']['localDate']

    description = events.get('info', 'no description provided')
    return render_template('event-details.html', 
                            img_url = img_url, 
                            event_name = event_name,
                            venues_list=venues_list,
                            classifications_list = classifications_list,
                            start_date=start_date,
                            event_url = event_url,
                            description = description)#, event=event,)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
