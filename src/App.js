import logo from './logo.svg';
import './App.css';
import React, { memo, useEffect, useState } from 'react';
import { refreshTokens } from './utils/backend'
import {
  BrowserRouter,
  Route,
  Routes
} from "react-router-dom";

import User from './views/User';

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
    <div>
      <BrowserRouter>
        <Routes>
          <Route path=":user" element={<User />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default memo(App)