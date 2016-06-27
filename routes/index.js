var express = require('express')
,	app		= express()
,	spawn	= require('child_process').spawn;

var irQ = [ [], [] ]
,	ir; // python process

module.exports = function() {

	initProc( irQ , 'ir.py' , 'IR' );

	/* route function */

	app.get('/', function(req, res) {
		res.render('index');
	});

	app.get('/ajax/load', function(req, res) {
		console.log( 'Load IR test ... ' );
		irQ[0].push( res );
		ir.stdin.write( 'Load\n' );
	});

	app.post('/ajax/test', function(req, res) {
		var d = req.body;
		console.log( 'Post test: ', d );
		irQ[1].push( res );
		ir.stdin.write( 'Eva ' + JSON.stringify(d) + '\n' );
	});

	return app;
};

var initProc = function( queue, proc_exe , name ) {
	console.log( 'Initializing python process' );
	ir	= spawn( 'python3', [ proc_exe ]);

	ir.stderr.on('data', function(data) {
		console.log( '(' + name + ':stderr)', data.toString() );
	});
	ir.stdout.on('data', function(data) {
		data = data.toString()
		console.log( '(' + name + ':stdout)', data );
		let type = parseInt( data.split( ' ' )[0] );
		if( type != 0 && type != 1 ) {
			console.log( ' --------- error input: ', data, ' : type: ', type );
			return;
		}
		popAndPass( queue[ type ] , data.substr(2,data.length) );
		
	});
	ir.stdout.on('end', function() {
		console.log( 'end of stdout\n' );
	});
	ir.on('close', function() {
		console.log( 'child [', name, '] closed.' );
		initProc( queue, proc_exe, name );
		console.log( 'Restart', proc_exe );	
	});


};

var popAndPass = function( queue , data ) {
	if( queue.length > 0 ) {
		queue[0].json( data.toString() );
		queue.splice(0,1);
	} else
		console.log( '---> empty wait queue but receive stdout' );
	
}
