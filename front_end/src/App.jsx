import React, {useEffect, useState} from 'react'
import Information from './components/information'
import Analysis from './components/analysis'
import Interaction from './components/interaction'
import Fetch from './fetch'
import './style/global.css'
import 'antd/dist/antd.css'

const App = () => {
    const [graph, setGraph] = useState({})
    const [option, setOptions] = useState([])
    const [author1, setAuthor1] = useState(null)
    const [author2, setAuthor2] = useState(null)
    useEffect(() => {
        // Fetch('/index').then()
        Fetch('/graph').then(
            res => {
                setGraph(res)
            })
        Fetch('/option').then(
            res => {
                setOptions(res)
            }
        )
    }, [])

    function handleAuthorChange(action) {
        const {target, value} = action
        if(target === 1){
            setAuthor1(value)
        }else if(target === 2){
            setAuthor2(value)
        }
    }

    return (<div>
        <Information/>
        <Analysis data={graph} onAuthorChange={handleAuthorChange}/>
        <Interaction
            option={option} author1={author1} author2={author2}
            onAuthorChange={handleAuthorChange}
        />
    </div>)
}
export default App;
