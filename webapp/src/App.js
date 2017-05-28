import React, { Component } from 'react';
import './App.css';
import SongItem from './components/song-item/song-item';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      songs: []
    }
  }

  componentDidMount() {
    this.setState({
      songs: [
        { id: 1, artist: 'Between the Buried and Me', title: 'Mirrors' },
        { id: 2, artist: 'Daft Punk', title: 'Get Lucky' },
        { id: 3, artist: 'Bon Iver', title: '10 d E A T h b R E a s T ⚄ ⚄' },
        { id: 4, artist: 'Bon Iver', title: 'Holocene' },
        { id: 5, artist: 'Pinegrove', title: 'Size of the Moon' },
      ]
    })
  }

  render() {
    let songs = this.state.songs;
    let songItems = songs.map(function(song) {
      return (
        <SongItem key={song.id} song={song} />
      );
    });

    return (
      <div className="App">
        <div className="header">
          <div>#songoftheday</div>
        </div>
        <div className="content">
          <ul>
            {songItems}
          </ul>
        </div>
      </div>
    );
  }
}

export default App;
