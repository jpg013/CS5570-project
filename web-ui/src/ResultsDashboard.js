import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import ClickRipple from './components/ClickRipple';
import Recoverability from './Recoverability';
import styles from './ResultsDashboard.module.css';

class ResultsDashboard extends React.PureComponent {
  static propTypes = {
    selectedTab: PropTypes.string.isRequired,
    history: PropTypes.object,
    onSelectTab: PropTypes.func.isRequired,
  }

  configureTopTabCxs(name) {
    const cxs = {}

    cxs[styles['ResultsDashboard-Top-Tab']] = true
    cxs[styles['ResultsDashboard-Top-Tab-Active']] = this.props.selectedTab === name;

    return cx(cxs);
  }

  render() {
    return (
      <div className={ styles['ResultsDashboard-Container']} >
        <div className={ styles['ResultsDashboard-Top']}>
          <div className={ this.configureTopTabCxs('recoverability') } onClick={ () => this.props.onSelectTab('recoverability') }>
            Recoverability
            <ClickRipple />
          </div>

          <div className={ this.configureTopTabCxs('serializability') } onClick={ () => this.props.onSelectTab('serializability') }>
            Serializability
            <ClickRipple />
          </div>

          <div className={ this.configureTopTabCxs('graphs') } onClick={ () => this.props.onSelectTab('graphs') }>
            Graphs
            <ClickRipple />
          </div>
        </div>
        <div className={ styles['ResultsDashboard-Body'] }>
          { this.props.selectedTab === 'recoverability' && <Recoverability history={ this.props.history} /> }
        </div>
      </div>
    );
  }
}

export default ResultsDashboard;
