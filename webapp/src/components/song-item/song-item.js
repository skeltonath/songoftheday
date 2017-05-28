import React, { Component } from 'react';
import './song-item.css';

class SongItem extends Component {
  render() {
    return (
      <li className="song-item">
        {this.props.song.artist}: {this.props.song.title}
      </li>
    );
  }
}

export default SongItem;