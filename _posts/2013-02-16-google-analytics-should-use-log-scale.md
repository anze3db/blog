---
layout: post
title: "Google Analytics should use log scale"
category: 
tags: [stats, math, blog]
---


Google Analytics is an awesome tool. I have the utmost respect for the googlers working on it every day.

There is a problem though. The graphs look okay if you have regular traffic throughout the month, but if you are a blogger that probably won't be the case. You will most likely have little to no traffic between blogs and then a huge surge of traffic when you write a new post. Especially if the *social web* gets a hold of it.

This is exactly what happend to me with my [The Chrome Javascript editor can do hot swapping](http://smotko.si/using-chrome-as-a-javascript-editor) blog post, and this is the resulting graph:

<div style="width:600px; display:inline-block;">
<span id="chart_div" style="width:700px; height:200px; display:inline-block;"></span>
</div>

As you can see, pretty much the only thing visible on this graph is the huge spike on the day I published the blog. Traffic on all the other days seems to be zero, with a small exception round 21 Jan when I published another blog. There is no way for me to tell how much traffic the other blog has gotten - somewhere below 2k would be my best guess from glancig at the graph.

The solution to this problem is amazingly simple. You use a **logarithmic scale** for the vertical axis:

<div style="width:600px; display:inline-block;">
<span id="log_chart_div" style="width:700px; height:200px; display:inline-block;"></span>
</div>

Now I can see everything - even the drop from 20 page views per day to 10. I can now tell exactly how much traffic the second blog post has gotten and the huge 12k spike still seems huge.

The funny thing is that all the chart/graph libraries have the option to use log scale - d3, pylab and even google charts all have it built in. It's weird that Google Analytics doesn't provide the option.

Am I the only one who prefers the second graph? Let me know what you think!

<script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Day', 'Visit'],
            ["1/17/13",39],
            ["1/18/13",30],
            ["1/19/13",25],
            ["1/20/13",79],
            ["1/21/13",588],
            ["1/22/13",144],
            ["1/23/13",69],
            ["1/24/13",44],
            ["1/25/13",22],
            ["1/26/13",11],
            ["1/27/13",26],
            ["1/28/13",46],
            ["1/29/13",21],
            ["1/30/13",16],
            ["1/31/13",24],
            ["2/1/13",11],
            ["2/2/13",11],
            ["2/3/13",10],
            ["2/4/13",11],
            ["2/5/13",19],
            ["2/6/13",26],
            ["2/7/13",12],
            ["2/8/13",13],
            ["2/9/13",8],
            ["2/10/13",6716],
            ["2/11/13",12084],
            ["2/12/13",829],
            ["2/13/13",704],
            ["2/14/13",415],
            ["2/15/13",352],
            ["2/16/13",202]
        ]);

        var options = {
          title: 'Normal Graph',
          hAxis: {title: 'Days', textPosition: 'none'},
          vAxis: {title: 'Visits'},
          legend: {position: 'none'}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
        
        options['title']="Log Scale Graph";
        options['vAxis']={title: 'Visits', logScale: true};
        
        var log_chart = new google.visualization.AreaChart(document.getElementById('log_chart_div'));
        log_chart.draw(data, options);
        
        }
  
</script>

