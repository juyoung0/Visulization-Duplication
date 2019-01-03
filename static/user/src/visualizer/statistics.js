/**
 * Created by dryji on 2017-02-20.
 * Bar chart and table for the selected units statistics
 */
(function (parent) {
    _.extend(parent,
        {
            createBarGraph: function () {
                // set the dimensions and margins of the graph
                var margin = {top: 20, right: 20, bottom: 30, left: 40},
                    width = $("div.bar-graph").parent().width() - margin.left - margin.right,
                    height = 500 - margin.top - margin.bottom;

                // set the ranges
                var x = d3.scaleLinear()
                    .range([0, width]);

                var y = d3.scaleBand()
                    .range([height, 0])
                    .padding(0.3);

                // append the svg object to the body of the page
                // append a 'group' element to 'svg'
                // moves the 'group' element to the top left margin
                var svg = d3.select("div.bar-graph").append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");

                // get the data
                d3.csv("scale.csv", function (error, data) {
                    if (error) throw error;

                    // format the data
                    data.forEach(function (d) {
                        d.count = +d.count;
                    });

                    // Scale the range of the data in the domains
                    y.domain(data.map(function (d) {
                        return d.gene;
                    }));
                    x.domain([0, d3.max(data, function (d) {
                        return d.count;
                    })]);

                    // append the rectangles for the bar chart
                    svg.selectAll(".bar")
                        .data(data)
                        .enter().append("rect")
                        .attr("class", "bar")
                        .attr("y", function (d) {
                            return y(d.gene);
                        })
                        .attr("height", y.bandwidth())
                        .attr("x", function (d) {
                            return 0
                        })
                        .attr("width", function (d) {
                            return x(d.count);
                        })
                        .attr("fill", function (d) {
                            return "rgb(0, 0, " + (d.count * 5) + ")";
                        });

                    // add the x Axis
                    svg.append("g")
                        .attr("transform", "translate(0," + height + ")")
                        .call(d3.axisBottom(x));

                    // add the y Axis
                    svg.append("g")
                        .call(d3.axisLeft(y));

                    visualizer.createBarTable(data);
                });
            }
        })
})(visualizer);
