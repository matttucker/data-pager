from subprocess import call

import couchdb
from datetime import datetime, timedelta
# from pprint import pprint


from yonder import app
from yonder.model import artist_model, follower_model, user_model, session_model, \
    genre_model, track_model, comment_model, playlist_model, authority_model
from yonder.model import album_model
from yonder.model import device_model
from yonder.model import metadata_artist_model


def check_test_databases():
    databases = [app.config['COUCHDB_MUSIC_DB'],
                 app.config['COUCHDB_USER_DB'],
                 app.config['COUCHDB_GAMES_DB'],
                 app.config['COUCHDB_EVENTS_DB'],
                 app.config['COUCHDB_DEVICES_DB']]

    for database in databases:
        if not database.startswith("test"):
            print "YIKES THESE ARE NOT TEST DATABASES! EXITING!"
            exit()


def setup_databases():

        check_test_databases()

        databases = [app.config['COUCHDB_MUSIC_DB'],
                     app.config['COUCHDB_USER_DB'],
                     app.config['COUCHDB_GAMES_DB'],
                     app.config['COUCHDB_EVENTS_DB'],
                     app.config['COUCHDB_DEVICES_DB']]

        # create test databases
        print "    Creating test databases..."
        couch = couchdb.Server(app.config['COUCHDB_SERVER'])

        # start with a clean slate so delete database
        try:
            for database in databases:
                couch.delete(database)

        except:
            pass

        try:
            for database in databases:
                couch.create(database)
        except:
            pass
        print "    Create design documents..."
         # change the _id of the couchapp design to update the design name that
         # will get pushed.
        database = "music-db"
        design = "music-db"
        cmd_str = "echo \"_design/{design}\" > ./db/{database}/designs/{design}/_id".format(
            database=database, design=design)
        call(cmd_str, shell=True)
        call(
            ["couchapp",
             "push",
             "./db/music-db/designs/music-db",
             app.config['COUCHDB_MUSIC_DB']])

        # couchapp push ./db/yonder-db/designs/yonder-db yonder-db
        database = "yonder-db"
        design = "yonder-db"
        cmd_str = "echo \"_design/{design}\" > ./db/{database}/designs/{design}/_id".format(
            database=database, design=design)
        call(cmd_str, shell=True)
        call(
            ["couchapp",
             "push",
             "./db/yonder-db/designs/yonder-db",
             app.config['COUCHDB_USER_DB']])

        database = "games"
        design = "games"
        cmd_str = "echo \"_design/{design}\" > ./db/{database}/designs/{design}/_id".format(
            database=database, design=design)
        call(cmd_str, shell=True)
        call(["couchapp", "push", "./db/{database}/designs/{design}".format(
            database=database, design=design), app.config['COUCHDB_GAMES_DB']])

        database = "events"
        design = "events"
        cmd_str = "echo \"_design/{design}\" > ./db/{database}/designs/{design}/_id".format(
            database=database, design=design)
        call(cmd_str, shell=True)
        call(["couchapp", "push", "./db/{database}/designs/{design}".format(
            database=database, design=design), app.config['COUCHDB_EVENTS_DB']])


def tear_down_databases(delete=True):
    check_test_databases()
    databases = [app.config['COUCHDB_MUSIC_DB'],
                 app.config['COUCHDB_USER_DB'],
                 app.config['COUCHDB_GAMES_DB'],
                 app.config['COUCHDB_EVENTS_DB'],
                 app.config['COUCHDB_DEVICES_DB'],
                 ]
    if delete:
        print "    Deleting test databases..."
        couch = couchdb.Server(app.config['COUCHDB_SERVER'])
        for database in databases:
            couch.delete(database)


def create_data():
        check_test_databases()

        from yonder import couchdb_utils as cdb
        from yonder import couchdb_utils_v2 as cdb2
        mdb = cdb.get_music_db()
        ddb = cdb2.get_devices_db()
        data = {}

        data['genres'] = []
        genre = genre_model.new('rock')
        mdb.save(genre)
        data['genres'].append(genre)

        genre = genre_model.new('metal')
        mdb.save(genre)
        data['genres'].append(genre)

        genre = genre_model.new('pop')
        mdb.save(genre)
        data['genres'].append(genre)

        data['artists'] = []
        #artist = artist_model.create('ACDC', echonest_id="ARWR05M1187B9951A2")
        artist = artist_model.new()
        artist["_id"] = "artist_acdc-1234"
        artist["name"] = "AC/DC"
        mdb.save(artist)
        data['artists'].append(artist)

        metadata_artist = metadata_artist_model.new(artist['_id'])
        metadata_artist["name"] = artist['name'],
        metadata_artist["bio"] = "bio"

        mdb.save(metadata_artist)

        data['albums'] = []
        for i in range(0, 5):
            album = album_model.new()
            album["_id"] = "album_{i}".format(i=i)
            album["title"] = "Album {i}".format(i=i)
            album["genre_names"] = [data['genres'][0]['name']]
            album["track_ids"] = ["track_0", "track_1"]
            mdb.save(album)
            data['albums'].append(album)

        data['tracks'] = []
        for i in range(0, 5):
            track = track_model.new()
            track["_id"] = "track_{i}".format(i=i)
            track['genre']={'_id':data['genres'][0]['_id'], 'name':data['genres'][0]['name']}
            track["genre_names"] = [data['genres'][0]['name']]
            track["artist"]["id"] = "artist_{i}".format(i=i)
            track["artist"]["name"] = "Artist {i}".format(i=i)
            track["album"]["id"] = data["albums"][0]["_id"]
            track["album"]["title"] = data["albums"][0]["title"]

            mdb.save(track)
            data['tracks'].append(track)

        db = cdb.get_db()

        #
        # create some users
        #

        data['devices'] = []
        data['users'] = []
        data['usernames'] = []
        data['passwords'] = []
        for i in range(0, 5):

            is_allowed = i != 4
            device = device_model.new(device_id='device_{i}'.format(i=i))
            device['is_allowed'] = is_allowed
            ddb.save(device)
            data['devices'].append(device)

            user = user_model.new_user(
                i, "facebook", "user[{i}]".format(i=i), "", "")
            user['devices'] = {}
            device_id = device['_id']
            country_code = 'us'
            user['devices'][device_id] = {}
            user['devices'][device_id]['home_region'] = country_code.lower()
            user['devices'][device_id]['last_region_checkin_date'] = (
                datetime.utcnow() - timedelta(days=180)).isoformat()
            data['users'].append(user)
            db.save(user)

            session = session_model.new_session(device_id, user['_id'])
            db.save(session)
            data['usernames'].append(session['_id'])
            data['passwords'].append("")

            # have all other users follow user 0;
            if i > 0:
                # have all other users follow user 0;
                follower = follower_model.set_following(
                    db, data['users'][0]['_id'], data['users'][i]['_id'], True)
                db.save(follower)

                # have user 0 follow other users
                follower = follower_model.set_following(
                    db, data['users'][i]['_id'], data['users'][0]['_id'], True)
                db.save(follower)

         #
        # create some authorities
        #
        data['authorities'] = []
        for i in range(0, 5):
            name = "authority[{i}]".format(i=i)
            authority = authority_model.new_authority(name, 'rock')
            data['authorities'].append(authority)
            db.save(authority)

        comment = comment_model.new_comment(
            data['users'][0]['_id'], data['tracks'][0]['_id'],
            data['tracks'][0]['genre']['_id'],
            data['tracks'][0]['artist']['id'],
            data['tracks'][0]['album']['id'],
            "test comment", False, 0, 1, None)
        db.save(comment)

        #
        # Playlists
        #
        data['playlists'] = []

        # create a playlist for user1
        tracks = data['tracks'][0:2]
        track_ids = []
        for track in tracks:
            track_ids.append(track['_id'])
        playlist = playlist_model.new_playlist(
            description="description",
            genre=None,
            image_url=None,
            image_urls=None,
            is_radio=False,
            release_date=None,
            title='title',
            track_ids=track_ids,
            user_id=data['users'][0]['_id'])
        playlist_model.update_playlist_artists_and_albums(playlist, tracks)
        # pprint(playlist)
        db.save(playlist)

        data['playlists'].append(playlist)

        playlist = playlist_model.new_playlist(
            description="description",
            genre=None,
            image_url=None,
            image_urls=None,
            is_radio=False,
            release_date=None,
            title='title',
            track_ids=track_ids,
            user_id=data['authorities'][0]['_id'])
        playlist_model.update_playlist_artists_and_albums(playlist, tracks)
        db.save(playlist)

        data['playlists'].append(playlist)

        playlist = playlist_model.new_playlist(
            description="hotshots playlist",
            genre=None,
            image_url=None,
            image_urls=None,
            is_radio=False,
            release_date=None,
            title='title',
            track_ids=track_ids,
            user_id=data['authorities'][0]['_id'])
        playlist['_id'] = playlist_model.HOT_SHOTS_PLAYLIST_ID
        playlist_model.update_playlist_artists_and_albums(playlist, tracks)
        db.save(playlist)

        data['playlists'].append(playlist)

        return data
