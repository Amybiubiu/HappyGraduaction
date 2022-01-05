import logo from './logo.svg';
// import './App.css';
import * as d3 from "d3";
import data from './static/output.json'
import { useEffect } from 'react'
function App() {
  const max = d3.max(data.map(item => item.category))

  useEffect(() => {
    // Step 3
    var svg = d3.select("svg")
              .attr("width", 1000)
              .attr("height", 1000);

    // Step 4
    svg.selectAll("circle")
      .data(data).enter()
      .append("circle")
      .attr("cx", function (d) { return d.x * 5 })
      .attr("cy", function (d) { return d.y * 5 })
      .attr("r", function (d) {
        // return Math.sqrt(d.val)/Math.PI 
        return 6
      })
      .attr("fill", function (d, i) {
        // colors
        // https://observablehq.com/@mbostock/color-ramp
        // https://github.com/d3/d3-scale-chromatic/blob/main/README.md#interpolateSinebow
        return d3.interpolateRainbow(d.category / (max - 1))
      });
     

    // Step 5
    // https://medium.com/@kj_schmidt/show-data-on-mouse-over-with-d3-js-3bf598ff8fc2
    // svg.selectAll("text")
    //   .data(data).enter()
    //   .append("text")
    //   .attr("x", function(d) {return d.x*5+6})
    //   .attr("y", function(d) {return d.y*5+4})
    //   .text(function(d) {return d.id})
    //   .style("font-family", "arial")
    //   .style("font-size", "12px")
    //   .on('mouseover', function (d, i) {
    //     d3.select(this).transition()
    //       .duration('50')
    //       .attr('opacity', '.85');
    //     //Makes the new div appear on hover:
    //     div.transition()
    //       .duration(50)
    //       .style("opacity", 1);
    //   })
    //   .on('mouseout', function (d, i) {
    //     d3.select(this).transition()
    //       .duration('50')
    //       .attr('opacity', '1');
    //     //Makes the new div disappear:
    //     div.transition()
    //       .duration('50')
    //       .style("opacity", 0);
    //   });

  }, [])
  return (
    <div className="App">
      <svg></svg>
    </div>
  );
}

export default App;
