import React from 'react';
import PropTypes from 'prop-types';
import styles from './LineGraph.module.css';
import cx from 'classnames';
import { axisLeft, axisBottom, scaleLinear, line, curveMonotoneX, select } from 'd3';

class LineGraph extends React.PureComponent {
  static propTypes = {
    dataSet: PropTypes.array.isRequired,
    xAxisText: PropTypes.string,
  }

  constructor(props) {
    super(props);
    this.componentRef = React.createRef();
  }

  componentDidMount() {
    const margin = {top: 50, right: 50, bottom: 50, left: 50};
    const { height, width } = this.componentRef.current.getBoundingClientRect()

    const domain = [1, this.props.dataSet[0].data.length + 1];
    const range = [0, width];

    const xScale = scaleLinear()
      .domain(domain)
      .range(range);

    const yScale = scaleLinear()
      .domain([0, 100])
      .range([height, 0]);

    const d3Line = line()
      .x(function(d, i) { return xScale(i+1); })
      .y(function(d) { return yScale(d.y); })
      .curve(curveMonotoneX)

    const svg = select(this.componentRef.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
      .attr("class", `x-axis ${styles['LineGraph-Axes-Tick']}`)
      .attr("transform", "translate(0," + height + ")")
      .call(axisBottom(xScale));

    svg.append("g")
      .attr("class", `y-axis ${styles['LineGraph-Axes-Tick']}`)
      .call(axisLeft(yScale));

    this.props.dataSet.forEach(curr => {
      const cns = {}
      cns[styles['LineGraph-Line']] = true;
      cns[styles[`LineGraph-Line-${curr.key}`]] = true;

      svg.append("path")
        .datum(curr.data)
        .attr("class", cx(cns))
        .attr("d", d3Line);
    })

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .attr("class", styles['LineGraph-Axes-Label'])
      .style("text-anchor", "middle")
      .text('Avg. % not RC/ACA/ST');

    svg.append("text")
      .attr("y", height)
      .attr("x", (width / 2) - 100)
      .attr("dy", "40px")
      .attr("class", styles['LineGraph-Axes-Label'])
      .style("text-anchor", "bottom")
      .text(this.props.xAxisText);
  }

  render() {
    return (
      <div className={ styles['LineGraph-Container'] } ref={ this.componentRef }>
        <div className={ styles['LineGraph-Legend'] }>
          <div className={ styles['LineGraph-Legend-Item'] }>
            <div className={ styles['LineGraph-Legend-Item-RC'] } />
            <div className={ styles['LineGraph-Legend-Item-Label'] }>Recoverable</div>
          </div>

          <div className={ styles['LineGraph-Legend-Item'] }>
            <div className={ styles['LineGraph-Legend-Item-ACA'] } />
            <div className={ styles['LineGraph-Legend-Item-Label'] }>Cascadeless</div>
          </div>

          <div className={ styles['LineGraph-Legend-Item']}>
            <div className={ styles['LineGraph-Legend-Item-ST'] } />
            <div className={ styles['LineGraph-Legend-Item-Label'] }>Strict</div>
          </div>
        </div>
      </div>
    )
  }
}

export default LineGraph;
