'use strict';

//Add environment vars or use standard values
var db = process.env.REDIS_URL || 'localhost'
var port = process.env.REDIS_PORT || 6379

const artistIds = require('./artist-ids');
const http = require('http');
const JSONStream = require('JSONStream');
const limit = 8; // The number of songs to retrieve for each artist
const parser = JSONStream.parse(['results', true]);

const nineteesIds = artistIds.ninetees;
const zeroesIds = artistIds.zeroes;
const nederlandsIds = artistIds.nederlands;
const dbvhIds = artistIds.dbvh;


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
    nineteesIds.concat(zeroesIds, nederlandsIds, dbvhIds).join() +
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
  if (artistId === nineteesIds[0]) {
    rooms.push('ninetees', 'zeroes-ninetees', 'mixed');
    // Set the skip counter (there is no need to update the rooms for the next pop artists)
    skip = nineteesIds.length - 1;
  } else if (artistId === zeroesIds[0]) {
    rooms.push('zeroes', 'zeroes-ninetees', 'mixed');
    skip = zeroesIds.length - 1;
  } else if (artistId === nederlandsIds[0]) {
    rooms.push('nederlands', 'mixed');
    skip = nederlandsIds.length - 1;
  } else {
    rooms.push('dbvh');
    skip = dbvhIds.length - 1;
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

rc.del(rooms, function(err) {
  if (err) {
    throw err;
  }
  process.stdout.write('Loading sample tracks... ');
  http.get(options, function(res) {
    res.pipe(parser);
  });
});
