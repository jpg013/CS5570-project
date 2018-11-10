import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import styles from './TextArea.module.css';

class TextArea extends React.PureComponent {
  static propTypes = {
    defaultVal: PropTypes.string,
  }

  constructor(props) {
    super(props);

    this.containerRef = React.createRef();
    this.areaSizeRef = React.createRef();
    this.inputRef = React.createRef();

    this.onInput = this.onInput.bind(this);
  }

  componentDidMount() {
    if (this.props.defaultVal) {
      this.inputRef.current.value = this.props.defaultVal;
      this.onInput();
    }

    this.inputRef.current.focus();
  }

  onInput() {
    this.areaSizeRef.current.innerHTML = this.inputRef.current.value + '\n';
  }

  render() {
    return (
      <div className={ styles['TextArea-Container'] } ref={ this.containerRef }>
        <textarea className={ styles['TextArea'] } onInput={ this.onInput } ref={ this.inputRef } />
        <div className={ styles['TextArea-Size'] } ref={ this.areaSizeRef }></div>
      </div>
    )
  }
}

export default TextArea;
