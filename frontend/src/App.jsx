import { useState } from 'react'
import './App.css'
import SpotifyRecommender from './components/SpotifyRecommender'
function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <SpotifyRecommender />
    </div>
  )
}

export default App;
