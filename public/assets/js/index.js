
var testid;
var inputid = 1;
var docN;

var addInput = function() {
	$('#input-box').append( '<br /><div class="12u$"><textarea class="talk-box" name="message" id="talk-' + inputid + '" placeholder="Say something." rows="4"></textarea></div>' );
	inputid ++;
};

var loadtest = function() {
	console.log('load start');

	loadin();

	$.get('/ajax/load', function( d ) {
		/* {index: 1, docs:[ [a,b],[a,b],[a,b], ...] } */
		data = JSON.parse( d );
		testid = data.index;
		console.log( data );
		console.log( data.index );

		docN = data.docs.length;
		for( var i in data.docs ) {
			$('#select-area').append( '<div class="panel panel-warning"><div class="panel-body"><table class="table table-striped selection" id="select-' + i + '"></table></div></div>' );
			for( var p in data.docs[i] )
				$('#select-' + i).append( '<tr id="select-' + i + '-' + p + '"><td>' + data.docs[i][p] + '</td></tr>' )
		}
		
		loadout();

		$( '#two' ).show();
		$( '#three' ).show();

		$( '#loadtest' ).hide();

		/* selection table */
		$('.selection td').on('click', function(e) {
			// this.id
			$(this).closest('table').find('.info').removeClass('info dsel');
			$(this).addClass('info dsel');
		});
	});
};

var eva = function() {

	var inputs = new Array();

	$('.dsel').each( function() {
		inputs.push( $(this).text() );
	});
	if( inputs.length != docN ) {
		alert( 'Please choose all options... NO 選擇困難！' )
		return;
	}

	$('.talk-box').each( function() {
		inputs.push( $(this).val() );
	});
	console.log( inputs );

	$.ajax({
        url: '/ajax/test',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            index: testid,
			input: inputs
	    }),
	    dataType: 'json'
    })
	.done(function(data) {
		console.log( 'GOT: ', data );
		var chart_input = {
		    datasets: [{
				data: JSON.parse(data),
				backgroundColor: [
					"#36A2EB",
					"#00840D",
					"#F4F118",
					"#F27107",
					"#87FF65",
					"#F72A2A"
				],
				label: 'My dataset' // for legend
			}],
			labels: [
				"國民黨",
				"民進黨",
				"時代力量",
				"親民黨",
				"綠黨",
				"社民黨"
			]
		};
		$('#four').show();
		var chart = new Chart(
			$('#chart-box'),{
			    data: chart_input,
			    type: 'polarArea',
			    options: {
					elements: {
						arc: {
						     borderColor: "#000000"
						}
					}
				}
			}
		);
	});

};

var loadin = function() {
	$('#loadtest').attr('disabled', true);
	$('#loadring').show();
};

var loadout = function() {
	$('#loadtest').attr('disabled', false);
	$('#loadring').hide();	
};

