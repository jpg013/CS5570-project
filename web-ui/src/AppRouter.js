import React from 'react';
import App from './App';
import { BrowserRouter as Router, Route} from "react-router-dom"

const ProjectInfo = () => <div>Project Info</div>

const AppRouter = () => (
  <Router>
    <div>
      <Route path="/" exact component={ App } />
      <Route path="/info" component={ ProjectInfo } />
    </div>
  </Router>
);

export default AppRouter;
