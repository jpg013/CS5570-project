import React from 'react';
import styles from './ScheduleDisplay.module.css';
import ArrowRightIcon from '../../icons/ArrowRightIcon';
import PropTypes from 'prop-types';

class ScheduleDisplay extends React.PureComponent {
  static propTypes = {
    schedule: PropTypes.array.isRequired,
    onClick: PropTypes.func.isRequired,
  }

  constructor(props) {
    super(props);

    this.renderScheduleItem = this.renderScheduleItem.bind(this);
  }

  renderScheduleItem(item, idx) {
    const isLastItem = (idx === (this.props.schedule.length - 1));

    return (
      <div className={ styles['ScheduleDisplay-Op'] } key={ idx }>
        <span className={ styles['ScheduleDisplay-Op-type'] }>{item.operation_type.toLowerCase()}</span>
        <span className={ styles['ScheduleDisplay-Op-tx'] }>{item.transaction_id}</span>
        { item.data_item && <span className={ styles['ScheduleDisplay-Op-data'] }>{item.data_item}</span> }
        { !isLastItem && <ArrowRightIcon /> }
      </div>
    )
  }

  render() {
    return (
      <div className={ styles.ScheduleDisplay } onClick={ this.props.onClick }>
        { this.props.schedule.map(this.renderScheduleItem) }
      </div>
    )
  }
}

export default ScheduleDisplay;
