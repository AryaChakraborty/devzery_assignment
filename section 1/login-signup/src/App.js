// import logo from './logo.svg';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './App.css';
import LoginSignup from './Components/LoginSignup/LoginSignup';
import Profile from './Components/Profile/Profile';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={LoginSignup} />
        <Route path="/profile" component={Profile} />
      </Switch>
    </Router>
    // <div>
    //   <LoginSignup />
    // </div>
  );
}

export default App;
