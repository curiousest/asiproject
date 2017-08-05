import React, { Component } from 'react';
import SearchInput from 'react-search-input';

export class RepositoryBoard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      repositories: [],
      repository_error: false,
    };
  }

  getRepositories(username) {
    fetch('http://localhost/github/repositories/?limit=10&order_by=-stargazers_count&username=' + username)
      .then(res => (res.json()))
      .then(data => (this.setState({ repositories: data })))
  };

  render() {
    var rows = [];
    for (var i=0; i < this.state.repositories.length; i++) {
      var r = this.state.repositories[i];
      rows.push(
        <tr><td>
        {renderRepository(r.name, r.description, r.language, r.stargazers_count, r.forks, r.html_url)}
        </td></tr>
      );
    }
    return (
      <div>
          <SearchInput className="search-input" onChange={this.getRepositories.bind(this)} />
          <table>{rows}</table>
      </div>
    );
  }
}

const boxstyle = {
  border: '1px',
  'border-style': 'solid'
}
function renderRepository (title, text, language, stars, forks, url) {
  return (
    <div style={boxstyle}>
      <span><a href="{url}"><bold>{title}</bold></a></span>
      <p>{text}</p>
      <p>{language}   ☆{stars}   ☊{forks}</p>
    </div>
  );
}
