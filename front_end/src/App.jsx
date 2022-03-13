import React from 'react'
import Information from './components/information'
import Analysis from './components/analysis'
import Interaction from './components/interaction'
import './style/global.css'
import 'antd/dist/antd.css'
const App = () => {
  return (<div>
    <Information />
    <Analysis />
    <Interaction />
  </div>)
}
export default App;
