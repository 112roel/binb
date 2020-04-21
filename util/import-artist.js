const artistIds = require("./artist-ids");
const http = require("http");
const JSONStream = require("JSONStream");
const limit = 7; // The number of songs to retrieve for each artist
const parser = JSONStream.parse(["results", true]);
const fs = require("fs");

const content = [];

const sixtiesIds = artistIds.sixties;
const seventiesIds = artistIds.seventies;
const eightiesIds = artistIds.eighties;
const ninetiesIds = artistIds.nineties;
const zeroesIds = artistIds.zeroes;
const tensIds = artistIds.tens;
const nederlandsIds = artistIds.nederlands;

function createJson(ids) {
  const options = {
    headers: { "content-type": "application/json" },
    host: "itunes.apple.com",
    // Look up multiple artists by their IDs and get `limit` songs for each one
    path:
      "/lookup?id=" +
      ids +
      "&entity=song&limit=" +
      limit +
      "&country=NL&sort=popular",
    port: 80,
  };

  http.get(options, function (res) {
    res.setEncoding("utf8");
    let rawData = "";
    res.on("data", (chunk) => {
      rawData += chunk;
    });
    res.on("end", () => {
      try {
        const parsedData = JSON.parse(rawData);
        //console.log(JSON.stringify(parsedData));
        output = JSON.stringify(parsedData);
        return output;
      } catch (e) {
        console.error(e.message);
      }
    });
  });
}

var test = createJson(seventiesIds);
setTimeout(function(){console.log(test)},3000);

