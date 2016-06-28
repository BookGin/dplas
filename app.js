var express			=		require('express')
, app				=		express()
, express           =     require('express')
, util              =     require('util')
, session           =     require('express-session')
, cookieParser      =     require('cookie-parser')
, bodyParser        =     require('body-parser')
, logger            =     require('morgan')
, path              =     require('path')
, favicon           =     require('serve-favicon')
, errorHandler      =     require('errorhandler')
, port				=		7122;



app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.set('port', port);
app.use(express.static(path.join(__dirname, 'public')));
  app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(cookieParser());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

var routes = require('./routes/index')();
app.use('/', routes);

app.listen(port, function () {
				console.log('ready on port ', port);
				});
