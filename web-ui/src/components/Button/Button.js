import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import styles from './Button.module.css';

class Button extends React.PureComponent {
  static propTypes = {
    classExtensions: PropTypes.string,
    type: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
  }

  static defaultProps = {
    classExtensions: '',
    type: 'default',
    text: '',
    onClick: () => undefined,
  }

  configureButtonClasses() {
    const buttonCxs = {};

    buttonCxs[styles.Button] = true;
    buttonCxs[styles['Button-Primary']] = this.props.type === 'primary';
    buttonCxs[this.props.classExtensions] = true;
    buttonCxs[styles['Button-WithIcon']] = !!this.props.children;

    return cx(buttonCxs);
  }

  render() {
    return (
      <div className={ this.configureButtonClasses() } onClick={ this.props.onClick }>
        { this.props.children && (
            <div className={ styles['Button-Icon'] }>
              { this.props.children }
            </div>
          )
        }
        { this.props.text }
      </div>
    )
  }
}

export default Button;
