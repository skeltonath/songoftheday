import React, { Component } from 'react';
import './App.css';
import SongItem from './components/song-item/song-item';
import 'whatwg-fetch';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      songs: []
    }
  }

  componentDidMount() {
    const url = '/api/songs';
    const opts = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    };
    fetch(url, opts)
      .then((resp) => resp.json())
      .then(function(data) {
        this.setState({ songs: data.songs });
      }.bind(this));
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
