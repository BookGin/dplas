import sys, json, jieba

#Read data from stdin
def read_in():
		line = sys.stdin.readline()
		return line

def main():
	sys.stderr.write(' >>>>>>  python runed \n')

	jieba.set_dictionary( 'dict.txt.big' )

	#get our data as an array from read_in()
	for line in sys.stdin:
		sys.stderr.write( 'get' + line + '\n' )
		print( " ".join( jieba.cut( line, cut_all=False ) ) ) 

		sys.stdout.flush()
		
	
	sys.stderr.write(' >>>>>>  python finished \n')

#start process
if __name__ == '__main__':
	main()
