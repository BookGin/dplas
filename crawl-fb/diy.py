from urllib.request import urlopen
import json
import sys
import dateutil.parser as dateparser
from dateutil.relativedelta import *
from datetime import *
import codecs
import os.path
import os

#########  Checking for valid arguments  #########

if len( sys.argv ) < 5:
  print( 'usage: ' + sys.argv[0] + ' -t [access token] -i [app list]' )
  sys.exit()

accessToken = ''
inputFile = ''

ari = 1
while ari < len( sys.argv ):
  if sys.argv[ ari ] == '-t':
    accessToken = sys.argv[ ari+1 ]
    ari += 2
  elif sys.argv[ ari ] == '-i':
    inputFile = sys.argv[ ari+1 ]
    ari += 2
  else:
    print( 'Unknown argument' + sys.argv[ ari ] )
    ari += 1

if len( accessToken ) * len( inputFile ) == 0:
  print( 'Losing some arguments' )
  print( 'usage: ' + sys.argv[0] + ' -t [access token] -i [app list]' )
  sys.exit()


##########  Define functions for retrieving data  ############

apps = {}
logfile = open( 'crawl.log', 'w', encoding='utf-8' )

def create_post_url( APP_ID, access_token ):
  # create init crawling url
  post_url = "https://graph.facebook.com/v2.6/" + APP_ID + '/posts?format=json&access_token=' + access_token
  return post_url

def render_to_json(graph_url):
  #render graph url call to JSON
  try:
    web_response = urlopen(graph_url)
    readable_page = web_response.read().decode('utf-8')
    json_data = json.loads(readable_page)
  except Exception:
    print( Exception )
    logfile.write( Exception + '\n' )

  return json_data

def withinAYear(base, timecmp):
  ya = base + relativedelta(years=-1)
  return timecmp.timetuple() > ya.timetuple()

def loadSrc():
  input = open( inputFile , 'r' )
  line = input.readline()
  while line:
    dir, num = line.split()
    files = []

    line = input.readline()
    for i in range( int(num) ):
        if os.path.exists( os.path.join( dir, line[:-1] ) ):
            print( dir + '/' + line[:-1] + '  already exists' )
            line = input.readline()
            continue
        files.append( line[:-1] )
        line = input.readline()
    apps[ dir ] = files

  input.close()

def getData( appId ):
  obj = {}
  basedata = render_to_json( "https://graph.facebook.com/v2.6/" + appId + '?format=json&access_token=' + accessToken )
  obj[ 'posts' ] = []
  obj[ 'name' ] = basedata[ 'name' ]
  print( 'Now ======>      ' + obj[ 'name' ] )


  post_url = create_post_url( appId, accessToken )
  json_data = render_to_json( post_url )

  timeNow = datetime.now()

  count = 0
  cont = True
  while cont:
    for post in json_data[ 'data' ]:
      try:
        if not withinAYear( timeNow , dateparser.parse( post[ 'created_time' ] ) ):
          print( post[ 'created_time' ] + ' is not in year')
          cont = False
          break
        # print( '----------------------- # ' + str(count) + ' --------------------------' )
        
        print( post[ 'created_time' ] + ' ---> ' + post[ 'message' ][:10] )
        obj[ 'posts' ].append( post['message'] )
        count = count + 1
        # print( '----------------------- @ ' + str( post[ 'created_time' ] )  + ' --------------------------' )

      except :
        continue

    # check for next paging
    if ('paging' in json_data) and ('next' in json_data[ 'paging' ]):
      next_url = json_data[ 'paging' ][ 'next' ]
      if len( next_url ) == 0:
        break
      json_data = render_to_json( next_url )
    else:
      break

    if len( json_data[ 'data' ] ) < 1:
      break
  print( appId + ' : ' + str(count) )
  
  return obj



# =========================================== #


# appId = 'mykmt'
# apps = [ 'mykmt', 'newpowerparty', 'dpptw', 'PFPTW', 'npsunion', 'tsu.org', 'newparty.antifake' ]
# apps = [ 'mykmt' ]

loadSrc() # load source list

allList = {}
for dir in apps:
  if not os.path.isdir( dir ):
    os.mkdir( dir )
  for f in apps[ dir ]:
    output = open( os.path.join(dir,f) , 'w' , encoding='utf-8' )
    ans = getData( f )
    print( f + ' of ' + dir + '  =  ' + str( len( ans[ 'posts' ] ) ) )

    json.dump( ans , output , ensure_ascii=False )
    output.close()

