
var testid;
var inputid = 1;

var addInput = function() {
	$('#input-box').append( '<br /><div class="12u$"><textarea name="message" id="talk-' + inputid + '" placeholder="Say something." rows="4"></textarea></div>' );
	inputid ++;

};

var loadtest = function() {
	console.log('load start');
	$('#loadtest').attr('disabled', true);
	$('#loadring').show();

	$.get('/ajax/load', function( d ) {
		/* {index: 1, docs:[ [a,b],[a,b],[a,b], ...] } */
		data = JSON.parse( d );
		testid = data.index;
		console.log( data );
		console.log( data.index );

		for( var i in data.docs ) {
			$('#select-area').append( '<div class="panel panel-warning"><div class="panel-body"><table class="table table-striped selection" id="select-' + i + '"></table></div></div>' );
			for( var p in data.docs[i] )
				$('#select-' + i).append( '<tr id="select-' + i + '-' + p + '"><td>' + data.docs[i][p] + '</td></tr>' )
		}
		
		$('#loadtest').attr('disabled', false);
		$('#loadring').hide();

		$( '#two' ).show();
		$( '#three' ).show();

		$( '#loadtest' ).hide();

		/* selection table */
		$('.selection tr').on('click', function(e) {
			// this.id
			$(this).siblings().removeClass('success');
			$(this).addClass('success');
		});
	});
};

