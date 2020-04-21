'use strict';

//Add environment vars or use standard values
var db = process.env.REDIS_URL || 'localhost'
var port = process.env.REDIS_PORT || 6379

const artistIds = require('./artist-ids');
const http = require('http');
const JSONStream = require('JSONStream');
const limit = 7; // The number of songs to retrieve for each artist
const parser = JSONStream.parse(['results', true]);

const sixtiesIds = artistIds.sixties; 
const seventiesIds = artistIds.seventies;
const eightiesIds = artistIds.eighties;
const ninetiesIds = artistIds.nineties;
const zeroesIds = artistIds.zeroes;
const tensIds = artistIds.tens;
const nederlandsIds = artistIds.nederlands;



const rc = require('redis').createClient({ host: db, port: port })
let rooms = require('../config').rooms;
let score;
let skip = 0; // Skip counter
let songId = 0;

const options = {
  headers: { 'content-type': 'application/json' },
  host: 'itunes.apple.com',
  // Look up multiple artists by their IDs and get `limit` songs for each one
  path:
    '/lookup?id=' +
    sixtiesIds.concat(seventiesIds).join() +
    '&entity=song&limit=' +
    limit + '&country=NL&sort=popular',
  port: 80
};

const options2 = {
  headers: { 'content-type': 'application/json' },
  host: 'itunes.apple.com',
  // Look up multiple artists by their IDs and get `limit` songs for each one
  path:
    '/lookup?id=' +
    eightiesIds.concat(ninetiesIds).join() +
    '&entity=song&limit=' +
    limit + '&country=NL&sort=popular',
  port: 80
};

const options3 = {
  headers: { 'content-type': 'application/json' },
  host: 'itunes.apple.com',
  // Look up multiple artists by their IDs and get `limit` songs for each one
  path:
    '/lookup?id=' +
    zeroesIds.concat(tensIds).join() +
    '&entity=song&limit=' +
    limit + '&country=NL&sort=popular',
  port: 80
};

const options4 = {
  headers: { 'content-type': 'application/json' },
  host: 'itunes.apple.com',
  // Look up multiple artists by their IDs and get `limit` songs for each one
  path:
    '/lookup?id=' +
    nederlandsIds.join() +
    '&entity=song&limit=' +
    limit + '&country=NL&sort=popular',
  port: 80
};


/**
 * Set the rooms in which the songs of a given artist will be loaded.
 */

const updateRooms = function(artistId) {
  rooms = ['mixed'];
  score = 0;
  if (artistId === sixtiesIds[0]) {
    rooms.push('sixties', 'hits', 'mixed');
    // Set the skip counter (there is no need to update the rooms for the next pop artists)
    skip = sixtiesIds.length - 1;
  } else if (artistId === seventiesIds[0]) {
    rooms.push('seventies', 'hits', 'mixed');
    skip = seventiesIds.length - 1;
  } else if (artistId === eightiesIds[0]) {
    rooms.push('eighties', 'hits', 'mixed');
    skip = eightiesIds.length - 1;
  } else if (artistId === ninetiesIds[0]) {
    rooms.push('nineties', 'hits', 'mixed');
    skip = ninetiesIds.length - 1;
  } else if (artistId === zeroesIds[0]) {
    rooms.push('zeroes', 'hits', 'mixed');
    skip = zeroesIds.length - 1;
  } else if (artistId === tensIds[0]) {
    rooms.push('tens', 'hits', 'mixed');
    skip = tensIds.length - 1;
  } else {
    rooms.push('nederlands', 'mixed');
    skip = nederlandsIds.length - 1;
  }
};


parser.on('data', function(track) {
  if (track.wrapperType === 'artist') {
    console.log('\x1b[36m%s\x1b[0m', track.artistName);
    if (skip) {
      skip--;
      return;
    }
    updateRooms(track.artistId);
    return;
  }

  //console.log(track.trackName);

  if (track.artistName && track.trackName && track.trackViewUrl && track.previewUrl) {
    rc.hmset(
        'song:' + songId,
        'artistName',
        track.artistName,
        'trackName',
        track.trackName,
        'trackViewUrl',
        track.trackViewUrl,
        'previewUrl',
        track.previewUrl,
        'artworkUrl60',
        track.artworkUrl60,
        'artworkUrl100',
        track.artworkUrl100
    );

    rooms.forEach(function (room) {
      const _score = room === 'mixed' ? songId : score;
      rc.zadd(room, _score, songId);
    });

  }else{
    process.stdout.write('ERRROR ERROR ERROR ERROR ERROR ERROR');
  }

  score++;
  songId++;
});

parser.on('end', function() {
  rc.quit();
  process.stdout.write('OK\n');
});

rc.del(rooms, async function(err) {
  if (err) {
    throw err;
  }
  process.stdout.write('Loading sample tracks part 1... ');
  http.get(options, function(res) {
    res.pipe(parser);
  });
  setTimeout(function(){
    http.get(options2, function(res) {
      res.pipe(parser);
    });
  }, 60000)
});
