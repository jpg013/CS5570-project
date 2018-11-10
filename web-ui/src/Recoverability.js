import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import axios from 'axios';
import Spinner from './components/Spinner';
import { transformScheduleToText } from './lib/data-transform';
import Button from './components/Button';
import styles from './Recoverability.module.css';

class Recoverability extends React.PureComponent {
  static propTypes = {
    history: PropTypes.object,
  }

  state = {
    inFlight: false,
    recovery_results: undefined,
  }

  constructor(props) {
    super(props);

    this.getRecoverability = this.getRecoverability.bind(this);
  }

  async getRecoverability() {
    if (this.state.inFlight) {
      return
    }

    this.setState(() => ({ inFlight: true, recovery_results: undefined }));

    const scheduleTxt = transformScheduleToText(this.props.history.schedule);

    const { data } = await axios.post('/recovery_report', { input: scheduleTxt })

    setTimeout(() => {
      this.setState(() => ({
        recovery_results: data[0],
        inFlight: false,
      }));
    }, 1000);
  }

  renderRecoverability() {
    const violations = this.state.recovery_results.filter(curr => curr.recoverable_value === 'IS_NOT_RECOVERABLE');
    const compliances = this.state.recovery_results.filter(curr => curr.recoverable_value !== 'IS_NOT_RECOVERABLE');
    const headerTxt = `History is${violations.length > 0 ? ' not ': ' '} recoverable.`;

    return (
      <div className={ styles['Recoverability-Violations-Result']} >
        <div className={ styles['Recoverability-Violations-Result-Header']} >
          { headerTxt }
        </div>

        <div className={ styles['Recoverability-Violations-Result-List']} >

        </div>
      </div>
    )
  }

  renderViolations() {
    if (!this.state.recovery_results || !this.state.recovery_results.length) {
      return null
    }

    // const recovery_violations = this.state.recovery_results.filter(curr => curr.recoverable_value === 'IS_NOT_RECOVERABLE');
    // const aca_violations = this.state.recovery_results.filter(curr => curr.cascade_value === 'IS_NOT_ACA');
    // const strict_violations = this.state.recovery_results.filter(curr => curr.strict_value === 'IS_NOT_STRICT');

    return (
      <div className={ styles['Recoverability-Violations'] }>
        { this.renderRecoverability() }
      </div>
    )
  }

  renderView() {
    if (!this.props.history) {
      return (
        <span className={ styles['Recoverability-NoInputMsg']} >Generate or enter a history schedule to see recoverability results.</span>
      )
    }

    return (
      <React.Fragment>
        <Button
          text="View Recoverability"
          onClick={ this.getRecoverability }
          />
        { this.state.recovery_results && this.renderViolations() }
      </React.Fragment>
    )
  }

  render() {
    return (
      <div className={ styles['Recoverability']} >
        { this.state.inFlight && <Spinner /> }
        { !this.state.inFlight && this.renderView() }
      </div>
    );
  }
}

export default Recoverability;
