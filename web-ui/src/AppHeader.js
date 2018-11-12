import React from 'react';
import HomeIcon from './icons/HomeIcon';
import GithubIcon from './icons/GithubIcon';
import ProjectInfoIcon from './icons/ProjectInfoIcon';
import styles from './AppHeader.module.css';
import { Link } from 'react-router-dom'

const appHeader = () => {
  return (
    <div className={ styles.appHeader }>
      <div className={ styles['appHeader-home'] }>
        <HomeIcon />
        <span className={ styles['appHeader-home-label'] }>
          concurrency control manager
        </span>
      </div>

      <div className={ styles['appHeader-options'] }>
        <Link to="/info" className={ styles['appHeader-options-link'] }>
          <ProjectInfoIcon />
          <span>Project Information</span>
        </Link>

        <a target="_blank" rel="noopener noreferrer" href="https://github.com/jpg013/concurrency-control-manager" className={ styles['appHeader-options-link'] }>
          <GithubIcon />
          <span>Source Code</span>
        </a>
      </div>
    </div>
  )
}

export default appHeader;
