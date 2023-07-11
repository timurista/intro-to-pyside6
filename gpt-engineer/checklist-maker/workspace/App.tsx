import React from 'react';
import { Provider } from 'mobx-react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Login';
import Checklist from './components/Checklist';
import ChecklistForm from './components/ChecklistForm';
import ChecklistSlide from './components/ChecklistSlide';
import { useChecklists, useLogin, useSaveChecklist } from './hooks';

const App: React.FC = () => {
  const { user, login, logout } = useLogin();
  const { checklists, fetchChecklists } = useChecklists();
  const { saveChecklist } = useSaveChecklist();

  return (
    <Provider {...{ user, login, logout, checklists, fetchChecklists, saveChecklist }}>
      <Router>
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/checklist" component={Checklist} />
          <Route path="/checklist-form" component={ChecklistForm} />
          <Route path="/checklist-slide" component={ChecklistSlide} />
        </Switch>
      </Router>
    </Provider>
  );
};

export default App;
