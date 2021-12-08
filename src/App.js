import logo from './logo.svg';
import './App.css';
import React, { memo, useEffect, useState } from 'react';
import { refreshTokens } from './utils/backend'

const componentDidMount = (setters) => {
  if (localStorage.lastAuthUser) {
    refreshTokens(localStorage.lastAuthUser, localStorage.refreshToken).then(resp => {
      resp.json().then(json => {
        localStorage.setItem("accessToken", json.access_token)
        localStorage.setItem("idToken", json.id_token)
        localStorage.setItem("tokenType", json.token_type)
        setters.setIsLoggedIn(true)
        setters.setUser(localStorage.lastAuthUser)
      })
    })

  }
}

function App(props) {
  const [user, setUser] = useState(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  const setters = {
    setUser: setUser,
    setIsLoggedIn: setIsLoggedIn
  }

  useEffect(async () => {
    componentDidMount(setters)
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default memo(App)