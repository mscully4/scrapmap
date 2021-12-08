import { 
  API_AUTH, 
} from './constants'

export const userLogin = (username, password) => {
  return fetch(`${API_AUTH}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  })
}

export const refreshTokens = (username, refreshToken) => {
  return fetch(`${API_AUTH}/refresh_tokens`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      refresh_token: refreshToken,
      username: username
    })
  })
}
