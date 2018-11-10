import React from 'react';
import Spinner from './components/Spinner';
import styles from './ScheduleInput.module.css';
import ScheduleDisplay from './components/ScheduleDisplay';
import TextArea from './components/TextArea';
import PropTypes from 'prop-types';

class ScheduleInput extends React.PureComponent {
  static propTypes = {
    onChanges: PropTypes.func.isRequired,
    onEdit: PropTypes.func.isRequired,
    status: PropTypes.string.isRequired,
    error: PropTypes.string,
    schedule: PropTypes.array.isRequired,
    strValue: PropTypes.string.isRequired,
    dataInFlight: PropTypes.bool.isRequired,
  }

  static defaultProps = {
    schedule: []
  }

  renderDisplay() {
    if (this.props.status === 'editing') {
      return (
        <TextArea
          defaultVal={ this.props.strValue }
          onBlur={ this.props.onChanges }
          error={ !!this.props.error }
          />
      )
    } else if (this.props.status === 'pristine') {
      return (
        <ScheduleDisplay
          schedule={ this.props.schedule }
          onClick={ this.props.onEdit }
          />
      )
    }

    return null;
  }

  render() {
    return (
      <div className={ styles['ScheduleInput'] }>
        {  this.props.dataInFlight ? <Spinner /> : this.renderDisplay()  }
      </div>
    );
  }
}

export default ScheduleInput;
