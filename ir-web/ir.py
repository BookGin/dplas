# coding=utf-8

import sys, json

count = 0

#Read data from stdin
def read_in():
		line = sys.stdin.readline()
		return json.load(line)

# random generate a json
def gen():
	global count

	# {index: 1, docs:[ [a,b],[a,b],[a,b], ...] } 
	obj = { 'index': count, 'docs': [] }
	for i in range(5):
		st = []
		st.append( str( 2*i*5566 ) )
		st.append( str((2*i+1)*5566 ) )
		obj[ 'docs' ].append( st )
	count += 1

	return obj

def evaluate( data ):
	# data = {index: 1, choice: "0101010010", input: ["我喜歡","jhk",...]}
	# this program should store which index store what docs
	# by the index and the choice seq 010101001
	# this function returns the result: [0.5, 0.0, 0.12, 0.3, 0.04, 0.04]

	return [0.5, 0.0, 0.12, 0.3, 0.04, 0.04]
	
	

def main():
	global count

	sys.stderr.write(' >>>>>>  IR server runed \n')

 	# jieba.set_dictionary( 'dict.txt.big' )

	# get our data as an array from read_in()
	for line in sys.stdin:

		if line.split()[0] == 'Load': # 0
		
			sys.stderr.write( 'Loading data #' + str(count) + '\n' )	
			print( '0 ' + json.dumps( gen() ) )

		elif line.split()[0] == 'Eva': # 1

			line = line.replace( 'Eva ', '', 1 )
			obj = json.load( line )
			sys.stderr.write( 'Evaluate data #' + obj[ 'index' ] + ': ' + obj[ 'result' ] + '\n' )
		else:
			sys.stderr.write( 'Got invalid: ' + line )

		sys.stdout.flush()
		
	sys.stderr.write('******************************\n')	
	sys.stderr.write(' >>>>>>  IR server finished \n')
	sys.stderr.write('******************************\n')	

#start process
if __name__ == '__main__':
	main()
	
