var express = require('express')
,	app		= express()
,	spawn	= require('child_process').spawn;

module.exports = function() {
	wait = [ [] ];
	py = initProc( wait , 'run.py' , 'Jieba' );

	irQ = [ [], [] ];
	ir = initProc( irQ , 'ir.py' , 'IR' );
	
	/* route function */

	app.get('/', function(req, res) {
		res.render('index');
	});
	app.get('/parse', function(req, res) {
		res.render('parse');
	});

	app.post('/ajax/parse', function(req, res) {
		var r = req.body.data;
		console.log( 'parse: ', r );
		wait[0].push( res );
		py.stdin.write( r + '\n' );
		//py.stdin.end();
	});

	app.get('/ajax/load', function(req, res) {
		console.log( 'Load IR test ... ' );
		irQ[0].push( res );
		ir.stdin.write( 'Load\n' );
	});

	app.post('/ajax/test', function(req, res) {
		var d = req.body.data;
		console.log( 'Post test: ', d );
		irQ[1].push( res );
		ir.stdin.write( 'Eva ' + d );
	});

	return app;
};

var initProc = function( queue, proc_exe , name ) {
	proc	= spawn( 'python3', [ proc_exe ]);

	proc.stderr.on('data', function(data) {
		console.log( '(' + name + ':stderr)', data.toString() );
	});
	proc.stdout.on('data', function(data) {
		data = data.toString()
		console.log( '(' + name + ':stdout)', data );
		let type = parseInt( data.split( ' ' )[0] );
		if( type != 0 && type != 1 ) {
			console.log( ' --------- error input: ', data, ' : type: ', type );
			return;
		}
		popAndPass( queue[ type ] , data.substr(2,data.length) );
		
	});
	proc.stdout.on('end', function() {
		console.log( 'end of stdout\n' );
	});
	proc.on('close', function() {
		console.log( 'child [', name, '] closed.' );
		proc = spawn( 'python3', [ proc_exe ]);
		console.log( 'Restart', proc_exe );	
	});

	return proc;

};

var popAndPass = function( queue , data ) {
	if( queue.length > 0 ) {
		queue[0].json( data.toString() );
		queue.splice(0,1);
	} else
		console.log( '---> empty wait queue but receive stdout' );
	
}
