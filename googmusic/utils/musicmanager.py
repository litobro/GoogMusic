from builtins import object
from gmusicapi import CallFailure, Mobileclient
from fuzzywuzzy import fuzz, process

class MusicManager(object):
    def __init__(self, client):
        self._client = client

    def _search(self, query_type, query):
        try:
            results = self._client.search(query)
        except CallFailure:
            return []

        hits_key = '%s_hits' % query_type

        if hits_key not in results:
            return []

        if query_type == 'song':
            query_type = 'track'

        return [x[query_type] for x in results[hits_key]] 

    def get_song(self, name, artist_name=None):
        if artist_name:
            name = '%s %s' % (artist_name, name)

        search = self._search('song', name)

        if len(search) == 0:
            return False

        return search[0]

    def get_artist(self, name):
        search = self._search('artist', name)

        if len(search) == 0:
            return False

        return search[0]['artistId']
