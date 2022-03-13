import React, {useEffect} from 'react'
import * as d3 from "d3"
import ForceGraph from "./ForceGraph";
import edges from '../static/edges.json'
import res from '../static/res.json'

// const data = {nodes: [
//     {id: "Myriel", category: 1}, {id: "Napoleon", category: 2}],
//     links: [{source: "Napoleon", target: "Myriel",value: 1}]}
const data = {nodes: res, links: edges}
const chart = ForceGraph(data, {
    nodeId: d => d.id,
    nodeGroup: d => d.category,
    nodeTitle: d => `${d.id}\n${d.category}`,
    linkStrokeWidth: l => Math.sqrt(l.value),
    width: 1000,
    height: 600,
    //invalidation // a promise to stop the simulation when the cell is re-run
})

console.log(chart)
const array = [].push(chart)
const Analysis = () => {
    useEffect(()=> {
        document.getElementById("container").append(chart)
    },[])
    return (<div className="page2">
        {/*<div dangerouslySetInnerHTML={{__html: chart.outerHTML}}/>*/}
        <div id="container" style={{padding: '2em'}}></div>
    </div>)
}
export default Analysis