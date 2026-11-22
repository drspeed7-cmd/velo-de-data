#!/usr/bin/env python3
"""
Build offline search database (SQLite + FTS5) from OSM PBF extract.

Usage:
  python3 build-search-db.py nordrhein-westfalen-latest.osm.pbf nrw.db

Requires: osmium (python3-osmium)
Install: pip install osmium
"""

import sys
import sqlite3
import osmium

class PlaceHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.places = []

    def node(self, n):
        tags = dict(n.tags)
        name = tags.get('name', '')
        if not name:
            return

        lat = n.location.lat
        lon = n.location.lon

        place = tags.get('place')
        if place in ('city', 'town', 'village', 'suburb', 'hamlet', 'neighbourhood'):
            self.places.append({
                'name': name,
                'street': '',
                'city': name if place in ('city', 'town') else '',
                'postcode': tags.get('postal_code', tags.get('addr:postcode', '')),
                'type': place,
                'latitude': lat,
                'longitude': lon,
            })
            return

        street = tags.get('addr:street', '')
        housenumber = tags.get('addr:housenumber', '')
        city = tags.get('addr:city', '')
        postcode = tags.get('addr:postcode', '')

        if street and housenumber:
            self.places.append({
                'name': f"{street} {housenumber}",
                'street': f"{street} {housenumber}",
                'city': city, 'postcode': postcode,
                'type': 'address',
                'latitude': lat, 'longitude': lon,
            })

        amenity = tags.get('amenity', '')
        shop = tags.get('shop', '')
        tourism = tags.get('tourism', '')

        if shop == 'bicycle':
            self._add(name, street, city, postcode, 'bicycle_shop', lat, lon)
        elif amenity == 'bicycle_repair_station':
            self._add(name, street, city, postcode, 'bicycle_repair', lat, lon)
        elif amenity == 'drinking_water':
            self._add(name or 'Trinkwasser', street, city, postcode, 'drinking_water', lat, lon)
        elif amenity == 'toilets':
            self._add(name or 'Toilette', street, city, postcode, 'toilets', lat, lon)
        elif amenity in ('cafe', 'restaurant', 'fast_food', 'biergarten'):
            self._add(name, street, city, postcode, amenity, lat, lon)
        elif tags.get('railway') == 'station':
            self._add(name, street, city, postcode, 'train_station', lat, lon)
        elif tourism == 'camp_site':
            self._add(name, street, city, postcode, 'camping', lat, lon)

    def _add(self, name, street, city, postcode, ptype, lat, lon):
        self.places.append({
            'name': name, 'street': street, 'city': city,
            'postcode': postcode, 'type': ptype,
            'latitude': lat, 'longitude': lon,
        })


def build_db(pbf_path, db_path):
    print(f"Reading OSM data from {pbf_path}...")
    handler = PlaceHandler()
    handler.apply_file(pbf_path, locations=True)
    print(f"Found {len(handler.places)} places")

    print(f"Building SQLite database {db_path}...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE places (
        name TEXT NOT NULL,
        street TEXT,
        city TEXT,
        postcode TEXT,
        type TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    )''')

    c.execute('CREATE INDEX idx_places_lat ON places(latitude)')
    c.execute('CREATE INDEX idx_places_lon ON places(longitude)')

    for p in handler.places:
        c.execute(
            'INSERT INTO places VALUES (?,?,?,?,?,?,?)',
            (p['name'], p['street'], p['city'], p['postcode'],
             p['type'], p['latitude'], p['longitude'])
        )

    c.execute('''CREATE VIRTUAL TABLE places_fts USING fts5(
        name, street, city, postcode,
        content='places', content_rowid='rowid'
    )''')

    c.execute('''INSERT INTO places_fts(rowid, name, street, city, postcode)
        SELECT rowid, name, street, city, postcode FROM places''')

    conn.commit()

    c.execute('SELECT COUNT(*) FROM places')
    total = c.fetchone()[0]
    print(f"Database built: {total} entries")
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.osm.pbf> <output.db>")
        sys.exit(1)
    build_db(sys.argv[1], sys.argv[2])
