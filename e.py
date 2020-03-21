#this step is trying to input the information of the shareholder, the price they paid and the investment amount they made. 
#The SQL will get a captable for us. 
#Then, we will start the calculation.

import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('/Users/sophia/desktop/captable.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Shareholders;
DROP TABLE IF EXISTS Round;
DROP TABLE IF EXISTS Investment;
DROP TABLE IF EXISTS Tracks;

CREATE TABLE Shareholders (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    title_id  INTEGER
);

CREATE TABLE Round (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE
);

CREATE TABLE Investment (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    shareholders_id  INTEGER,
    title_id INTEGER,
    price INTEGER, investment INTEGER
);

CREATE TABLE Tracks (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title_id  INTEGER,
    shareholders_id INTEGER,
    exitvalue INTEGER,
    percentage INTEGER
);
''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = '/Users/sophia/desktop/vc.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    title = lookup(entry, 'Title')
    price = lookup(entry, 'Price')
    investment = lookup(entry, 'Investment')

    if name is None or title is None:
        continue

    print(name, title, price, investment)

    cur.execute('''INSERT OR IGNORE INTO Round (title) 
        VALUES ( ?)''', ( title, ) )
    cur.execute('SELECT id FROM Round WHERE title = ? ', (title, ))
    title_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Shareholders (name, title_id) 
        VALUES ( ?, ? )''', ( name, title_id ) )
    cur.execute('SELECT id FROM Shareholders WHERE name = ? ', (name, ))
    shareholders_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Investment
        (shareholders_id, title_id, price, investment) 
        VALUES ( ?, ?, ?, ? )''',
        ( shareholders_id, title_id, price, investment ) )

    cur.execute('''INSERT OR REPLACE INTO Tracks
        (shareholders_id, title_id) 
        VALUES ( ?, ? )''',
        ( shareholders_id, title_id ) )

    conn.commit()
