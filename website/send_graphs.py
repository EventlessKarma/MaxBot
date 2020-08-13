import database


def send_graphs(user_id: int) -> str:

    to_send = """<!DOCTYPE HTML>
<html>
<head>  
<script>
window.onload = function () {{
	
var chart1 = new CanvasJS.Chart("chartContainer", {{
	animationEnabled: true,
	
	title:{{
		text:"todays d20 rolls"
	}},
	axisX:{{
		interval: 1
	}},
	axisY2:{{
		interlacedColor: "rgba(1,77,101,.2)",
		gridColor: "rgba(1,77,101,.1)",
		title: "roll frequency"
	}},
	data: [{{
		type: "bar",
		name: "rolls",
		axisYType: "secondary",
		color: "#014D65",
		{}
		
		
		
		]
	}}]
}});
chart1.render();
}}

</script>
</head>

<body>
<div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
</body>
</html>
""".format(data_points(get_rolls(user_id, 20)))

    return to_send


def get_rolls(user_id, dice=20):

    db = database.RollDatabase()
    r = db.get_rolls(user_id, dice)
    return r


def data_points(db_rolls: list) -> str:

    db_rolls = db_rolls[1:-1]
    to_return = "dataPoints: [ "

    for i in range(len(db_rolls)):
        to_return += "{{ y: {}, label: '{}' }},".format(db_rolls[i], i + 1)

    to_return = to_return[:-1]

    return to_return

