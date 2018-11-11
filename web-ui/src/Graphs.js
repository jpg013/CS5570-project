import React from 'react';
import axios from 'axios';
import Spinner from './components/Spinner';
import Button from './components/Button';
import styles from './Graphs.module.css';
import LineGraph from './components/LineGraph';

class Graphs extends React.PureComponent {
  state = {
    inFlight: false,
    graph_results: undefined,
  }

  constructor(props) {
    super(props);

    this.fetchGraphs = this.fetchGraphs.bind(this);
  }

  async fetchGraphs() {
    if (this.state.inFlight) {
      return
    }

    this.setState(() => ({ inFlight: true, graph_results: undefined }));

    try {
      const { data } = await axios.get('/generate_graphs')

      setTimeout(() => {
        this.setState(() => ({
          graph_results: data,
          inFlight: false,
        }));
      }, 1000);
    } catch(e) {
      console.log(e);
    }
  }

  renderTransactionGraph() {
    if (!this.state.graph_results) {
      return
    }

    const { transaction_graph } = this.state.graph_results;
    const dataset = [
      {
        name: 'not recoverable',
        key: 'rc',
        data: transaction_graph.map(curr => ({ y: curr.not_recoverable_percent }))
      },
      {
        name: 'not cacadeless',
        key: 'aca',
        data: transaction_graph.map(curr => ({ y: curr.not_cacadeless_percent }))
      },
      {
        name: 'not strict',
        key: 'st',
        data: transaction_graph.map(curr => ({ y: curr.not_strict_percent }))
      },
    ]

    return (
      <div className={ styles['Graphs-Chart']}>
        <LineGraph dataSet={ dataset } xAxisText="Max Transaction Count per History"/>
      </div>
    )
  }

  renderDataSetGraph() {
    if (!this.state.graph_results) {
      return
    }

    const { data_set_graph: results } = this.state.graph_results;
    const dataset = [
      {
        name: 'not recoverable',
        key: 'rc',
        data: results.map(curr => ({ y: curr.not_recoverable_percent }))
      },
      {
        name: 'not cacadeless',
        key: 'aca',
        data: results.map(curr => ({ y: curr.not_cacadeless_percent }))
      },
      {
        name: 'not strict',
        key: 'st',
        data: results.map(curr => ({ y: curr.not_strict_percent }))
      },
    ]

    return (
      <div className={ styles['Graphs-Chart']}>
        <LineGraph dataSet={ dataset } xAxisText="Max data item count per transaction"/>
      </div>
    )
  }

  renderGraphs() {
    return (
      <div className={ styles['Graphs-Container']}>
        { this.renderTransactionGraph() }
        { this.renderDataSetGraph() }
      </div>
    )
  }

  renderView() {
    return (
      <React.Fragment>
        <Button
          text="View Graphs"
          onClick={ this.fetchGraphs }
          />
        { this.state.graph_results && this.renderGraphs() }
      </React.Fragment>
    )
  }

  render() {
    return (
      <div className={ styles['Graphs']} >
        { this.state.inFlight && <Spinner /> }
        { !this.state.inFlight && this.renderView() }
      </div>
    );
  }
}

export default Graphs;
