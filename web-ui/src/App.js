import React from 'react';
import AppHeader from './AppHeader';
import Button from './components/Button'
import BuildIcon from './icons/BuildIcon';
import GenerateIcon from './icons/GenerateIcon';
import ScheduleIcon from './icons/ScheduleIcon';
import ChevronRightIcon from './icons/ChevronRightIcon';
import ResultsDashboard from './ResultsDashboard';
import styles from './App.module.css';
import ScheduleInput from './ScheduleInput'
import { transformScheduleToText } from './lib/data-transform';
import axios from 'axios';

class App extends React.PureComponent {
  state = {
    schedule: {
      inFlight: false,
      status: 'init',
      error: undefined,
      value: [],
      strValue: '',
    },
    history: undefined,
    results: {
      selectedTab: 'recoverability',
    }
  }

  constructor(props) {
    super(props);

    this.onGenerateHistory = this.onGenerateHistory.bind(this);
    this.onScheduleEdit = this.onScheduleEdit.bind(this);
    this.onChanges = this.onChanges.bind(this);
    this.onSelectTab = this.onSelectTab.bind(this);
  }

  async requestHistoryBuilder(input) {
    try {
      this.setState(prevState => {
        return {
          ...prevState,
          history,
          schedule: {
            ...prevState.schedule,
            strValue: input,
            inFlight: true,
            error: undefined,
          }
        };
      });

      const { data: history } = await axios.post('/build_history', { input });

      setTimeout(() => {
        this.setState(prevState => {
          return {
            ...prevState,
            history,
            schedule: {
              ...prevState.schedule,
              inFlight: false,
              status: 'pristine',
              value: history.schedule,
              error: undefined,
              strValue: transformScheduleToText(history.schedule),
            }
          };
        })
      }, 1000);
    } catch(e) {
      setTimeout(() => {
        this.setState(prevState => {
          return {
            ...prevState,
            schedule: {
              ...prevState.schedule,
              inFlight: false,
              status: 'editing',
              error: e.message,
            }
          };
        });
      }, 1000)
    }
  }

  async fetchGeneratedHistory() {
    this.setState(prevState => {
      return {
        ...prevState,
        history: undefined,
        schedule: {
          ...prevState.schedule,
          inFlight: true,
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
            inFlight: false,
            status: 'pristine',
            error: undefined,
            strValue: transformScheduleToText(history.schedule),
            value: history.schedule,
          }
        };
      });
    }, 1000)
  }

  onGenerateHistory() {
    if (this.state.schedule.inFlight) {
      return;
    }

    this.fetchGeneratedHistory()
  }

  onScheduleEdit() {
    if (this.state.schedule.inFlight) {
      return;
    }

    this.setState(prevState => {
      return {
        ...prevState,
        schedule: {
          ...prevState.schedule,
          status: 'editing',
        }
      }
    })
  }

  onSelectTab(name) {
    this.setState(prevState => {
      return {
        ...prevState,
        results: {
          ...prevState.results,
          selectedTab: name,
        }
      }
    })
  }

  onChanges(str) {
    if (this.state.schedule.inFlight) {
      return;
    }

    if (this.state.schedule.strValue.trim() === str.trim() || !str) {
      this.setState(prevState => {
        return {
          ...prevState,
          schedule: {
            ...prevState.schedule,
            status: 'pristine',
          }
        };
      });
    } else {
      this.requestHistoryBuilder(str);
    }
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
              <div className={ styles['App-banner-actions-label'] }>
                <span>Select history option</span>
                <ChevronRightIcon />
              </div>

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
            dataInFlight={ this.state.schedule.inFlight }
            status={ this.state.schedule.status }
            schedule={ this.state.schedule.value }
            strValue={ this.state.schedule.strValue }
            onEdit={ this.onScheduleEdit }
            onChanges={ this.onChanges }
            error={ this.state.schedule.error }
          />

          <ResultsDashboard
            selectedTab={ this.state.results.selectedTab}
            onSelectTab={ this.onSelectTab }
            history={ this.state.history }
            />
        </div>
      </div>
    );
  }
}

export default App;
