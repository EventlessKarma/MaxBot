var http = require('http');
var fs = require('fs');
console.log("Starting")
http.createServer(function (req, res) {
  fs.readFile('test.html', function(err, data) {
    if (err) { console.log("error")}
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    return res.end();
  });
}).listen(9999); 