import React from 'react';
import AppHeader from './AppHeader';
import Button from './components/Button'
import BuildIcon from './icons/BuildIcon';
import GenerateIcon from './icons/GenerateIcon';
import ScheduleIcon from './icons/ScheduleIcon';
import Spinner from './components/Spinner';
import styles from './App.module.css';
import ScheduleDisplay from './components/ScheduleDisplay';
import axios from 'axios';

class App extends React.PureComponent {
  state = {
    status: 'waiting',
    history: undefined,
    activeTab: ''
  }

  constructor(props) {
    super(props);

    this.onGenerateHistory = this.onGenerateHistory.bind(this);
  }

  async fetchGeneratedHistory() {
    this.setState(() => ({
      status: 'fetching',
      history: undefined // reset the history
    }));

    const { data } = await axios.get('/generate_history');

    setTimeout(() => {
      this.setState(() => ({
        status: 'waiting',
        history: data,
      }));
    }, 1000)
  }

  onGenerateHistory() {
    if (this.state.status !== 'waiting') {
      return
    }

    this.fetchGeneratedHistory()
  }

  render() {
    return (
      <div className={ styles['App'] }>
        <AppHeader />

        <div className={ styles['App-container'] }>
          <div className={ styles['App-banner']}>
            <div className={ styles['App-banner-icon']}>
              <ScheduleIcon />
            </div>
            <span className={ styles['App-banner-title'] }>History Analysis</span>

            <div className={ styles['App-banner-actions'] }>
              <span className={ styles['App-banner-created-txt'] }>
                Select history option
              </span>

              <Button
                text="Generate History"
                type="primary"
                classExtensions={ styles['App-banner-actions-first'] }
                onClick={ this.onGenerateHistory }
              >
                <GenerateIcon />
              </Button>

              <Button
                text="Input History"
                type="default"
              >
                <BuildIcon />
              </Button>
            </div>
          </div>

          <div className={ styles['App-History'] }>
            { this.state.status === 'fetching' && <Spinner /> }
            { this.state.history && <ScheduleDisplay schedule={ this.state.history.schedule }/> }
          </div>
        </div>
      </div>
    );
  }
}

export default App;
