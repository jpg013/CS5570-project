import React from 'react';
import Spinner from './components/Spinner';
import styles from './ScheduleInput.module.css';
import ScheduleDisplay from './components/ScheduleDisplay';
import TextArea from './components/TextArea';
import { transformScheduleToText } from './lib/data-transform';
import PropTypes from 'prop-types';

class ScheduleInput extends React.PureComponent {
  static propTypes = {
    onChanges: PropTypes.func.isRequired,
    onEdit: PropTypes.func.isRequired,
    status: PropTypes.string.isRequired,
    error: PropTypes.string,
    schedule: PropTypes.array.isRequired,
  }

  static defaultProps = {
    schedule: []
  }

  constructor(props) {
    super(props);

    this.onTextAreaBlur = this.onTextAreaBlur.bind(this);
  }

  onTextAreaBlur() {

  }

  renderTextArea() {
    return <TextArea defaultVal={ transformScheduleToText(this.props.schedule) }  />
  }

  renderDisplay() {
    if (!this.props.schedule.length) {
      return null;
    }

    return <ScheduleDisplay
      schedule={ this.props.schedule }
      onClick={ this.props.onEdit }
      />
  }

  render() {
    return (
      <div className={ styles['ScheduleInput'] }>
        { this.props.status === 'in-flight' && <Spinner />  }
        { this.props.status === 'waiting' && this.renderDisplay() }
        { this.props.status === 'edit' && this.renderTextArea() }
      </div>
    );
  }
}

export default ScheduleInput;
