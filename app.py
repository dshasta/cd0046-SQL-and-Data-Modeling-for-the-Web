#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from flask import jsonify
import traceback
from models import Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
from extensions import db
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database DONE

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# See models.py

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  recent_artists = Artist.query.order_by(Artist.created_at.desc()).limit(10).all()
  recent_venues = Venue.query.order_by(Venue.created_at.desc()).limit(10).all()

  return render_template('pages/home.html', recent_artists=recent_artists, recent_venues=recent_venues)



#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.  DONE
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

#   data=[{
#     "city": "San Francisco",
#     "state": "CA",
#     "venues": [{
#       "id": 1,
#       "name": "The Musical Hop",
#       "num_upcoming_shows": 0,
#     }, {
#       "id": 3,
#       "name": "Park Square Live Music & Coffee",
#       "num_upcoming_shows": 1,
#     }]
#   }, {
#     "city": "New York",
#     "state": "NY",
#     "venues": [{
#       "id": 2,
#       "name": "The Dueling Pianos Bar",
#       "num_upcoming_shows": 0,
#     }]
#   }]

    all_venues = Venue.query.all()
    venue_data = {}
    for venue in all_venues:
        key = (venue.city, venue.state)
        if key not in venue_data:
            venue_data[key] = {
                "city": venue.city,
                "state": venue.state,
                "venues": []
            }

        num_upcoming_shows = Show.query.filter(Show.venue_id == venue.id, Show.start_time > datetime.now()).count()

        venue_data[key]["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })

    data = list(venue_data.values())
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" DONE

#   response={
#     "count": 1,
#     "data": [{
#       "id": 2,
#       "name": "The Dueling Pianos Bar",
#       "num_upcoming_shows": 0,
#     }]
#   }
    
    # 1. Get the search term from the form
    search_term = request.form.get('search_term', '')

    # 2. Query the database for matching venues
    matching_venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()

    # 3. Build the response data
    response = {
        "count": len(matching_venues),
        "data": []
    }

    for venue in matching_venues:
        num_upcoming_shows = Show.query.filter(
            Show.venue_id == venue.id, 
            Show.start_time > datetime.now()
        ).count()

        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows,
        })

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id  DONE
  
#   data1={
#     "id": 1,
#     "name": "The Musical Hop",
#     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#     "address": "1015 Folsom Street",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "123-123-1234",
#     "website": "https://www.themusicalhop.com",
#     "facebook_link": "https://www.facebook.com/TheMusicalHop",
#     "seeking_talent": True,
#     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     "past_shows": [{
#       "artist_id": 4,
#       "artist_name": "Guns N Petals",
#       "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#       "start_time": "2019-05-21T21:30:00.000Z"
#     }],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
#   }
#   data2={
#     "id": 2,
#     "name": "The Dueling Pianos Bar",
#     "genres": ["Classical", "R&B", "Hip-Hop"],
#     "address": "335 Delancey Street",
#     "city": "New York",
#     "state": "NY",
#     "phone": "914-003-1132",
#     "website": "https://www.theduelingpianos.com",
#     "facebook_link": "https://www.facebook.com/theduelingpianos",
#     "seeking_talent": False,
#     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#     "past_shows": [],
#     "upcoming_shows": [],
#     "past_shows_count": 0,
#     "upcoming_shows_count": 0,
#   }
#   data3={
#     "id": 3,
#     "name": "Park Square Live Music & Coffee",
#     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#     "address": "34 Whiskey Moore Ave",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "415-000-1234",
#     "website": "https://www.parksquarelivemusicandcoffee.com",
#     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#     "seeking_talent": False,
#     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "past_shows": [{
#       "artist_id": 5,
#       "artist_name": "Matt Quevedo",
#       "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#       "start_time": "2019-06-15T23:00:00.000Z"
#     }],
#     "upcoming_shows": [{
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-01T20:00:00.000Z"
#     }, {
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-08T20:00:00.000Z"
#     }, {
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-15T20:00:00.000Z"
#     }],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 1,
#   }
#   data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  
  
    # Query venue based on the venue_id
    venue = Venue.query.get(venue_id)

    # Check if venue exists
    if not venue:
        return render_template('errors/404.html'), 404

    # Get current time to filter past and upcoming shows
    current_time = datetime.now()

    past_shows_query = Show.query.join(Artist).filter(
        Show.venue_id == venue_id,
        Show.start_time < current_time
    ).all()

    upcoming_shows_query = Show.query.join(Artist).filter(
        Show.venue_id == venue_id,
        Show.start_time > current_time
    ).all()

    # Format past shows
    past_shows = [{
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in past_shows_query]

    # Format upcoming shows
    upcoming_shows = [{
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in upcoming_shows_query]

    # Handle genres as comma-separated string
    genres_list = venue.genres.split(',')

    # Construct the response object
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres_list,  # Use the split list here
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,  # Corrected to match your model field
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_talent_description,  # Corrected to match your model field
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        # Fetch data from form
        form_data = request.form
        
        # Convert the list of genres to a comma-separated string
        genres_list = form_data.getlist('genres')
        genres_string = ",".join(genres_list)
        
        new_venue = Venue(
            name=form_data['name'],
            city=form_data['city'],
            state=form_data['state'],
            address=form_data['address'],
            phone=form_data['phone'],
            genres=genres_string,
            facebook_link=form_data['facebook_link'],
            image_link=form_data['image_link'],
            website_link=form_data['website_link'],
            seeking_talent=form_data.get('seeking_talent') in ['y', 'on'],
            seeking_talent_description=form_data['seeking_description']
        )

        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + form_data['name'] + ' was successfully listed!')

    except Exception as e:
        print(e)  # This will print the error to your terminal where the Flask app is running.
        db.session.rollback()
        flash('An error occurred. Venue ' + form_data['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return redirect(url_for('index'))


#def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead  DONE
  # TODO: modify data to be the data object returned from db insertion DONE

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead. DONE
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')


  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.  DONE

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage DONE

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        # Query the venue with the provided id
        venue = Venue.query.get(venue_id)
        
        # If the venue doesn't exist, abort with 404
        if not venue:
            abort(404)
        
        # Delete the venue
        db.session.delete(venue)
        
        # Commit the session
        db.session.commit()

    except:
        # If any exception occurs, roll back the session
        db.session.rollback()
        flash('An error occurred. Venue could not be deleted.', 'error')
        
    finally:
        # Close the session
        db.session.close()

    # Redirect to the homepage after deletion
    return jsonify({"success": True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database  DONE
  
#   data=[{
#     "id": 4,
#     "name": "Guns N Petals",
#   }, {
#     "id": 5,
#     "name": "Matt Quevedo",
#   }, {
#     "id": 6,
#     "name": "The Wild Sax Band",
#   }]
    
    # Query all artists from the database
    artists_query = Artist.query.all()

    # Transform the query result to the expected format
    data = [{"id": artist.id, "name": artist.name} for artist in artists_query]

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.  DONE
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
#   response={
#     "count": 1,
#     "data": [{
#       "id": 4,
#       "name": "Guns N Petals",
#       "num_upcoming_shows": 0,
#     }]
#   }


    search_term = request.form.get('search_term', '')
    
    # Fetch artists that match the search term using case-insensitive search
    matching_artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    
    # Prepare the data for the response
    data = []
    for artist in matching_artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            # Counting the shows that are yet to start for each artist
            "num_upcoming_shows": len([show for show in artist.shows if show.start_time > datetime.now()]),
        })

    response = {
        "count": len(matching_artists),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id  DONE
  
#   data1={
#     "id": 4,
#     "name": "Guns N Petals",
#     "genres": ["Rock n Roll"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "326-123-5000",
#     "website": "https://www.gunsnpetalsband.com",
#     "facebook_link": "https://www.facebook.com/GunsNPetals",
#     "seeking_venue": True,
#     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     "past_shows": [{
#       "venue_id": 1,
#       "venue_name": "The Musical Hop",
#       "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#       "start_time": "2019-05-21T21:30:00.000Z"
#     }],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
#   }
#   data2={
#     "id": 5,
#     "name": "Matt Quevedo",
#     "genres": ["Jazz"],
#     "city": "New York",
#     "state": "NY",
#     "phone": "300-400-5000",
#     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#     "seeking_venue": False,
#     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#     "past_shows": [{
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#       "start_time": "2019-06-15T23:00:00.000Z"
#     }],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
#   }
#   data3={
#     "id": 6,
#     "name": "The Wild Sax Band",
#     "genres": ["Jazz", "Classical"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "432-325-5432",
#     "seeking_venue": False,
#     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     "past_shows": [],
#     "upcoming_shows": [{
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#       "start_time": "2035-04-01T20:00:00.000Z"
#     }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#       "start_time": "2035-04-08T20:00:00.000Z"
#     }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#       "start_time": "2035-04-15T20:00:00.000Z"
#     }],
#     "past_shows_count": 0,
#     "upcoming_shows_count": 3,
#   }
#   data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

    artist = Artist.query.get(artist_id)
    if not artist:
        flash('Artist not found')
        return redirect(url_for('index'))

    # Extracting basic artist information
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_venue_description,  # Updated this line
        "image_link": artist.image_link,
    }

    # Extracting show-related information

    past_shows = []
    upcoming_shows = []

    for show in artist.shows:
        show_data = {
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        if show.start_time <= datetime.now():
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    data["past_shows_count"] = len(past_shows)
    data["upcoming_shows_count"] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    
    # Fetch artist by artist_id from the database
    artist_data = Artist.query.get(artist_id)
    
    if not artist_data:
        # Handle the case where the artist doesn't exist
        flash('Artist with ID {} not found.'.format(artist_id))
        return redirect(url_for('index'))
    
    # Populate form data from the artist's details
    form.name.data = artist_data.name
    form.genres.data = artist_data.genres.strip("[]").split(", ") if artist_data.genres else []
    form.city.data = artist_data.city
    form.state.data = artist_data.state
    form.phone.data = artist_data.phone
    form.website_link.data = artist_data.website_link
    form.facebook_link.data = artist_data.facebook_link
    form.seeking_venue.data = artist_data.seeking_venue
    form.seeking_description.data = artist_data.seeking_venue_description
    form.image_link.data = artist_data.image_link

    return render_template('forms/edit_artist.html', form=form, artist=artist_data)
  
#   artist={
#     "id": 4,
#     "name": "Guns N Petals",
#     "genres": ["Rock n Roll"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "326-123-5000",
#     "website": "https://www.gunsnpetalsband.com",
#     "facebook_link": "https://www.facebook.com/GunsNPetals",
#     "seeking_venue": True,
#     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
#   }

  # TODO: populate form with fields from artist with ID <artist_id>  DONE

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # Fetch the artist by artist_id from the database
    artist = Artist.query.get(artist_id)
    
    if not artist:
        flash('Artist with ID {} not found.'.format(artist_id))
        return redirect(url_for('index'))

    # Fetch the form data
    form = ArtistForm(request.form)
    
    try:
        # Update artist details with form data
        artist.name = form.name.data
        artist.genres = ', '.join(form.genres.data)
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website_link = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_venue_description = form.seeking_description.data
        artist.image_link = form.image_link.data

        # Commit changes to database
        db.session.commit()
        
        flash('Artist {} was successfully updated!'.format(artist.name))

    except Exception as e:  # Capture the exception into variable 'e'
        db.session.rollback()
        # Print detailed error information
        print("Exception occurred:", e)
        print(traceback.format_exc())  # This line prints the traceback
        
        flash('An error occurred. Artist {} could not be updated.'.format(artist.name))
    
    finally:
        # Close the session
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes DONE

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    
    # Fetch the venue by venue_id from the database
    venue_data = Venue.query.get(venue_id)
    
    if not venue_data:
        # Handle the case where the venue doesn't exist
        flash('Venue with ID {} not found.'.format(venue_id))
        return redirect(url_for('index'))
    
    # Populate form data from the venue's details
    form.name.data = venue_data.name
    form.genres.data = venue_data.genres.split(", ") if venue_data.genres else []
    form.address.data = venue_data.address
    form.city.data = venue_data.city
    form.state.data = venue_data.state
    form.phone.data = venue_data.phone
    form.website_link.data = venue_data.website_link
    form.facebook_link.data = venue_data.facebook_link
    form.seeking_talent.data = venue_data.seeking_talent
    form.seeking_description.data = venue_data.seeking_talent_description
    form.image_link.data = venue_data.image_link

    return render_template('forms/edit_venue.html', form=form, venue=venue_data)
  
#   venue={
#     "id": 1,
#     "name": "The Musical Hop",
#     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#     "address": "1015 Folsom Street",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "123-123-1234",
#     "website": "https://www.themusicalhop.com",
#     "facebook_link": "https://www.facebook.com/TheMusicalHop",
#     "seeking_talent": True,
#     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
#   }

  # TODO: populate form with values from venue with ID <venue_id> DONE

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Fetch the venue by venue_id from the database
    venue = Venue.query.get(venue_id)
    
    if not venue:
        flash('Venue with ID {} not found.'.format(venue_id))
        return redirect(url_for('index'))

    # Fetch the form data
    form = VenueForm(request.form)
    
    try:
        # Update venue details with form data
        venue.name = form.name.data
        venue.genres = ', '.join(form.genres.data)
        venue.address = form.address.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.website_link = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_talent_description = form.seeking_description.data
        venue.image_link = form.image_link.data

        # Commit changes to database
        db.session.commit()
        
        flash('Venue {} was successfully updated!'.format(venue.name))

    except Exception as e:  # Capture the exception into variable 'e'
        db.session.rollback()
        # Print detailed error information
        print("Exception occurred:", e)
        print(traceback.format_exc())  # This line prints the traceback
        
        flash('An error occurred. Venue {} could not be updated.'.format(venue.name))
    
    finally:
        # Close the session
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes  DONE

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
       
    # Create an instance of ArtistForm
    form = ArtistForm(request.form)

    # Print the form data to the terminal
    print(form.data)     

    # Validate form data
    if form.validate():
        try:
            # Create new Artist instance with form data
            genres_string = ','.join(form.genres.data)
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=genres_string,
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website_link=form.website_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_venue_description=form.seeking_description.data
            )
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully listed!')
        except Exception as e:
            db.session.rollback()
            # Log the exception for debugging
            print(e)
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
        finally:
            db.session.close()
    else:
        # If the form data isn't valid, flash error messages and re-render the form
        for error in form.errors.values():
            flash(error[0])
        return render_template('forms/new_artist.html', form=form)

    return redirect(url_for('index'))



#def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead  DONE
  # TODO: modify data to be the data object returned from db insertion  DONE

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.') DONE
  #return render_template('pages/home.html')

# EXTRA BONUS Add Delete button on artist page
 
@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        # Query the artist with the provided id
        artist = Artist.query.get(artist_id)
        
        # If the artist doesn't exist, abort with 404
        if not artist:
            abort(404)
        
        # Delete the artist
        db.session.delete(artist)
        
        # Commit the session
        db.session.commit()

    except:
        # If any exception occurs, roll back the session
        db.session.rollback()
        flash('An error occurred. Artist could not be deleted.', 'error')
        
    finally:
        # Close the session
        db.session.close()

    # Return a success response as JSON
    return jsonify({"success": True})  


#  Shows
#  ----------------------------------------------------------------

# displays list of shows at /shows
# TODO: replace with real venues data.  DONE

@app.route('/shows')
def shows():
    # Fetch all shows from the database
    all_shows = Show.query.all()

    # Iterate over each show to populate the data list
    data = []
    for show in all_shows:
        data.append({
            "id": show.id,
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)



#   data=[{
#     "venue_id": 1,
#     "venue_name": "The Musical Hop",
#     "artist_id": 4,
#     "artist_name": "Guns N Petals",
#     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     "start_time": "2019-05-21T21:30:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "artist_id": 5,
#     "artist_name": "Matt Quevedo",
#     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#     "start_time": "2019-06-15T23:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "artist_id": 6,
#     "artist_name": "The Wild Sax Band",
#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     "start_time": "2035-04-01T20:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "artist_id": 6,
#     "artist_name": "The Wild Sax Band",
#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     "start_time": "2035-04-08T20:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "artist_id": 6,
#     "artist_name": "The Wild Sax Band",
#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     "start_time": "2035-04-15T20:00:00.000Z"
#   }]

@app.route('/shows/create')

# commenting out to update route with auto-populate functionality
# def create_shows():
#   # renders form. do not touch.
#   form = ShowForm()
#   return render_template('forms/new_show.html', form=form)

def create_shows():
    # Fetch the list of all artists and venues
    artists = Artist.query.order_by(Artist.name).all()
    venues = Venue.query.order_by(Venue.name).all()

    # renders form.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form, artists=artists, venues=venues)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # Fetching artist and venue as before

    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']

    # Construct the start_time from the separate date and time fields
    date = f"{request.form['year']}-{request.form['month']}-{request.form['day']}"
    time = f"{request.form['hour']}:{request.form['minute']} {request.form['period']}"
    start_time_string = f"{date} {time}"
    
    # Convert the string to a datetime object
    start_time = datetime.strptime(start_time_string, '%Y-%m-%d %I:%M %p')
    
    # Check if artist_id and venue_id exist
    artist_exists = db.session.query(db.exists().where(Artist.id == artist_id)).scalar()
    venue_exists = db.session.query(db.exists().where(Venue.id == venue_id)).scalar()

    if not artist_exists or not venue_exists:
        flash('Error: Invalid Artist ID or Venue ID.')
        return redirect(url_for('create_shows'))

    # If both IDs exist, proceed with show creation
    try:
        new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return redirect(url_for('shows'))

#def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead  DONE

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')  DONE


  # *BONUS* adding ability to edit and delete shows

@app.route('/shows/<int:show_id>/edit')
def edit_show(show_id):
    # Fetch the show data
    show = Show.query.get(show_id)
    if not show:
        return redirect(url_for('shows'))
    
    # Fetch all artists and venues for the dropdowns
    artists = Artist.query.all()
    venues = Venue.query.all()
    
    return render_template('forms/edit_show.html', show=show, artists=artists, venues=venues)


    # Create option for individual show pages to enable editing/deleting

@app.route('/shows/<int:show_id>')
def show_show(show_id):
    # Query the database to get the show by its ID
    show = Show.query.get(show_id)
    if not show:
        # Handle the case where the show does not exist
        flash('Show not found.')
        return redirect(url_for('index'))  # Assuming 'index' is the route name for your homepage
    
    # If the show exists, render its details page
    return render_template('pages/show_show.html', show=show)


@app.route('/shows/<int:show_id>/delete', methods=['POST'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    if not show:
        flash('Show does not exist.')
        return redirect(url_for('shows'))
    try:
        db.session.delete(show)
        db.session.commit()
        flash('Show was successfully deleted!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be deleted.')
    finally:
        db.session.close()
    return redirect(url_for('shows'))

# Route to handle Form Submission and update the show

@app.route('/shows/<int:show_id>/edit', methods=['POST'])
def update_show(show_id):
    try:
        show = Show.query.get(show_id)
        if not show:
            # Handle case where the show doesn't exist.
            abort(404)

        # Retrieve date and time inputs
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        day = int(request.form.get('day'))
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        period = request.form.get('period')

        if period == "PM" and hour != 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0

        show.start_time = datetime(year, month, day, hour, minute)
        show.artist_id = request.form.get('artist_id')
        show.venue_id = request.form.get('venue_id')

        db.session.commit()

        flash('Show was successfully updated!')
    except Exception as e:
        db.session.rollback()
        print(e)  # Optionally, use logging instead of print
        flash('An error occurred. Show could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('shows'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
