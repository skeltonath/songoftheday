const express = require('express');
const app = express();

app.get('/api/songs', function(req, res) {
  res.send({
    songs: [
      { id: 1, artist: 'Between the Buried and Me', title: 'Mirrors' },
      { id: 2, artist: 'Daft Punk', title: 'Get Lucky' },
      { id: 3, artist: 'Bon Iver', title: '10 d E A T h b R E a s T ⚄ ⚄' },
      { id: 4, artist: 'Bon Iver', title: 'Holocene' },
      { id: 5, artist: 'Pinegrove', title: 'Size of the Moon' },
    ]
  });
});

let server = app.listen(4000, function() {
  let host = server.address().address;
  let port = server.address().port;

  console.log('App listening at http://%s:%s', host, port);

  setInterval(function() {
    console.log('still alive...')
  }, 1000 * 30);
});