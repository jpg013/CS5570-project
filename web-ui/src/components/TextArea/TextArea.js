import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import styles from './TextArea.module.css';

class TextArea extends React.PureComponent {
  static propTypes = {
    defaultVal: PropTypes.string,
    onBlur: PropTypes.func.isRequired,
    error: PropTypes.bool
  }

  constructor(props) {
    super(props);

    this.containerRef = React.createRef();
    this.areaSizeRef = React.createRef();
    this.inputRef = React.createRef();

    this.onInput = this.onInput.bind(this);
    this.onChanges = this.onChanges.bind(this);
    this.onKeyPress = this.onKeyPress.bind(this);
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

  onChanges() {
    return this.props.onBlur(this.inputRef.current.value);
  }

  onKeyPress(e) {
    if (e && e.which === 13) {
      e.preventDefault();
      e.stopPropagation();
      this.inputRef.current.blur();
    }
  }

  configureTextAreaCxs() {
    const cxNames = {};
    cxNames[styles['TextArea']] = true;
    cxNames[styles['TextArea-error']] = this.props.error === true;

    return cx(cxNames);
  }

  render() {
    return (
      <div className={ styles['TextArea-Container'] } ref={ this.containerRef }>
        <div className={ styles['TextArea-Label'] }>Input history in the following format: w1[x] r2[x] c1 a2</div>
        { this.props.error && <span className={ styles['TextArea-error-message']}>Invalid history input </span> }
        <textarea
          onKeyPress={ this.onKeyPress }
          className={ this.configureTextAreaCxs() }
          onBlur={ this.onChanges }
          onInput={ this.onInput }
          ref={ this.inputRef }
          />
        <div className={ styles['TextArea-Size'] } ref={ this.areaSizeRef }></div>
      </div>
    )
  }
}

export default TextArea;
