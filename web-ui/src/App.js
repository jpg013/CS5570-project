import React from 'react';
import AppHeader from './AppHeader';
import Button from './components/Button'
import BuildIcon from './icons/BuildIcon';
import GenerateIcon from './icons/GenerateIcon';
import ScheduleIcon from './icons/ScheduleIcon';
import styles from './App.module.css';
import ScheduleInput from './ScheduleInput'
import axios from 'axios';

class App extends React.PureComponent {
  state = {
    schedule: {
      status: 'waiting',
      error: undefined,
      value: []
    },
    history: undefined,
  }

  constructor(props) {
    super(props);

    this.onGenerateHistory = this.onGenerateHistory.bind(this);
    this.onScheduleEdit = this.onScheduleEdit.bind(this);
    this.onChanges = this.onChanges.bind(this);
  }

  async requestHistoryBuilder(input) {
    if (this.state.schedule.status !== 'edit') {
      return
    }

    this.setState(prevState => {
      return {
        ...prevState,
        schedule: {
          ...prevState.schedule,
          status: 'building',
        }
      }
    });

    try {
      const { data: history } = await axios.post('/build_history', { input });

      this.setState(prevState => {
        return {
          ...prevState,
          history,
          schedule: {
            ...prevState.schedule,
            status: 'waiting',
            value: history.schedule,
          }
        };
      })
    } catch(e) {
      console.log(e)
    }
  }

  async fetchGeneratedHistory() {
    this.setState(prevState => {
      return {
        ...prevState,
        schedule: {
          ...prevState.schedule,
          status: 'in-flight',
          error: undefined,
          value: [],
        }
      };
    });

    const { data: history } = await axios.get('/generate_history');

    setTimeout(() => {
      this.setState(prevState => {
        return {
          ...prevState,
          history,
          schedule: {
            ...prevState.schedule,
            status: 'waiting',
            value: history.schedule,
          }
        };
      });
    }, 1000)
  }

  onGenerateHistory() {
    if (this.state.schedule.status === 'in-flight') {
      return;
    }

    this.fetchGeneratedHistory()
  }

  onScheduleEdit() {
    if (this.state.schedule.status !== 'waiting') {
      return;
    }

    this.setState(prevState => {
      return {
        ...prevState,
        schedule: {
          ...prevState.schedule,
          status: 'edit',
        }
      }
    })
  }

  onChanges(input) {
    if (!input) {
      return;
    }

    this.requestHistoryBuilder(input);
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
                onClick={ this.onScheduleEdit }
              >
                <BuildIcon />
              </Button>
            </div>
          </div>

          <ScheduleInput
            status={ this.state.schedule.status }
            schedule={ this.state.schedule.value }
            onEdit={ this.onScheduleEdit }
            onChanges={ this.onChanges }
            error={ this.state.schedule.error }
          />
        </div>
      </div>
    );
  }
}

export default App;
