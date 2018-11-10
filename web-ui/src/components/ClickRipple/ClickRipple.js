import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import './ClickRipple.css';

class ClickRipple extends React.PureComponent {
  static propTypes = {
    theme: PropTypes.string.isRequired
  };

  static defaultProps = {
    theme: 'dark'
  }

  constructor(props) {
    super(props);

    this.componentRef = React.createRef();
    this.handleMouseDown = this.handleMouseDown.bind(this);
  }

  getRippleContainerDimensions() {
    const {
      height,
      width,
      top,
      left
    } = this.componentRef.current.getBoundingClientRect();

    const diameter = Math.max(height, width);

    return {
      top,
      left,
      width,
      height,
      diameter,
      cx: width / 2,
      cy: height / 2
    };
  }

  handleMouseDown(evt) {
    const {
      top,
      left,
      diameter,
      height,
      width,
      cx,
      cy
    } = this.getRippleContainerDimensions();

    const offsetY = cy - (evt.pageY - top - document.documentElement.scrollTop);
    const offsetX = cx - (evt.pageX - left - document.documentElement.scrollLeft);
    const centerOffset = Math.max(Math.abs(offsetX), Math.abs(offsetY)) * 2;
    const adjustedDiameter = (diameter + centerOffset) + ((diameter + centerOffset) * .5); // adjust for border radius
    const translateX = -((adjustedDiameter - width) / 2);
    const translateY = -((adjustedDiameter - height) / 2);
    const rippleEffectRef = document.createElement('span');

    rippleEffectRef.classList.add('clickRipple-effect');
    rippleEffectRef.style.width = `${adjustedDiameter}px`;
    rippleEffectRef.style.height = `${adjustedDiameter}px`;
    rippleEffectRef.style.transform = `translate(${translateX - offsetX}px, ${translateY - offsetY}px)`;

    this.componentRef.current.appendChild(rippleEffectRef);

    let isEnterAnimationDone = false;

    function handleAnimationEnd(evt) {
      if (!rippleEffectRef) {
        return;
      }

      return (evt.animationName === 'click-ripple-exit') ? cleanupRef() : isEnterAnimationDone = true;
    }

    function handleMouseUp() {
      rippleEffectRef.style.animationName = 'click-ripple-exit';
      rippleEffectRef.style.animationFillMode = 'forwards';
      rippleEffectRef.style.animationTimingFunction = 'cubic-bezier(0.4, 0, 0.2, 1)';

      if (!isEnterAnimationDone) {
        rippleEffectRef.style.animationDelay = '180ms';
        rippleEffectRef.style.animationDuration = '600ms';
      } else {
        rippleEffectRef.style.animationDelay = '0ms';
        rippleEffectRef.style.animationDuration = '200ms';
      }

      rippleEffectRef.parentElement.removeEventListener('mouseleave', handleMouseLeave);
    }

    function handleMouseLeave(e) {
      if (!rippleEffectRef || !rippleEffectRef.parentElement) {
        return;
      }
      cleanupRef();
    }

    function addRefEvents() {
      rippleEffectRef.parentElement.addEventListener('mouseup', handleMouseUp);
      rippleEffectRef.parentElement.addEventListener('mouseleave', handleMouseLeave);
      rippleEffectRef.addEventListener('animationend', handleAnimationEnd);
    }

    function cleanupRef() {
      if (!rippleEffectRef) {
        return;
      }
      rippleEffectRef.parentElement.removeEventListener('mouseup', handleMouseUp);
      rippleEffectRef.parentElement.removeEventListener('mouseleave', handleMouseLeave);
      rippleEffectRef.removeEventListener('animationend', handleAnimationEnd);
      rippleEffectRef.parentElement.removeChild(rippleEffectRef);
    }

    requestAnimationFrame(() => {
      const enterRef = document.createElement('span');

      enterRef.classList.add('clickRipple-effect-enter');
      rippleEffectRef.appendChild(enterRef);
    });

    addRefEvents();
  }

  configStyles() {
    const styleExtensions = {};

    styleExtensions['clickRipple-dark'] = this.props.theme === 'dark';
    styleExtensions['clickRipple-light'] = this.props.theme === 'light';

    return cx('clickRipple', styleExtensions);
  }

  render() {
    return (
      <span
        className={this.configStyles()}
        ref={this.componentRef}
        onMouseDown={this.handleMouseDown}
        >
      </span>
    );
  }
}

export default ClickRipple;
