#!/usr/bin/python3

import sys, getopt
import subprocess
import os



class SolveFieldFallback():
	
	__solve_field_bin = "/usr/bin/solve-field"
	__custom_L = "2.2000"
	__custom_H = "2.5000"
	__custom_objs = "100"
	__custom_L_enable = False
	__custom_H_enable = False
	__custom_objs_enable = False
	
	__solve_fields_sargs = "hvD:o:b:fpOKJN:Z:i:n:U:7L:H:u:8:c:E:q:Q:3:4:5:d:l:r6:z:9C:S:I:M:R:j:B:W:P:k:AV:ygTt:m:F:w:e:X:Y:s:a"
	__solve_fields_largs =   [ "help","verbose", 
							   "dir=", "out=",
							   "backend-config=", "config=",
							   "batch", "files-on-stdin",
							   "no-plots", "plot-scale=", 
							   "plot-bg=", "overwrite",
							   "continue", "skip-solved",
							   "fits-image", "new-fits=",
							   "kmz=", "scamp=", 
							   "scamp-config=", "index-xyls=",
							   "just-augment", "axy=", 
							   "temp-axy", "timestamp",
							   "no-delete-temp", "scale-low=",
							   "scale-high=", "scale-units=",
							   "parity=", "code-tolerance=",
							   "pixel-error=", "quad-size-min=",
							   "quad-size-max=", "odds-to-tune-up=",
							   "odds-to-solve=", "odds-to-reject=",
							   "odds-to-stop-looking=", "use-sextractor",
							   "sextractor-config=", "sextractor-path=",
							   "ra=", "dec=", "radius=", "depth=",
							   "objs=", "cpulimit=", "resort", "extension=",
							   "downsample=", "no-background-subtraction",
							   "sigma=", "nsigma=", "no-remove-lines", 
							   "uniformize=", "no-verify-uniformize", 
							   "no-verify-dedup", "cancel=", "solved=",
							   "solved-in=", "match=", "rdls=",
							   "sort-rdls=", "tag=", "tag-all",
							   "scamp-ref=", "corr=", "wcs=",
							   "pnm=", "keep-xylist=", "dont-augment",
							   "verify=", "verify-ext=", "no-verify",
							   "guess-scale", "crpix-center", "crpix-x=",
							   "crpix-y=", "no-tweak", "tweak-order=",
							   "temp-dir=", "fields=", "width=", "height=",
							   "x-column=", "y-column=", "sort-column=", "sort-ascending" 
							   ]
							  

	def help(self):
		print ("solve-field wrapper, supported options:\n"
			   "\t -h, --help (solve-field help)\n"
			   "\t -u, --scale-units <units>\n"
			   "\t -L, --scale-low <scale>\n"
			   "\t -H, --scale-high <scale>\n"
			   "\t -z, --downsample <int>\n"
			   "\t--objs <int>\n"
			   "\t -b, --backend-config <filename>\n"
			   "\t -W, --wcs <filename>\n"
			   "\t -k, --keep-xylist <filename>\n"
			   "\t -C, --cancel <filename>\n\n"
			   "the other solve-field options are bypassed and set from script.\n"
			   "For options information see solve-field man. Bye")

	def write_last_command(self, last_command):

		script_path = os.path.dirname(os.path.realpath(__file__))
		last_command_path = os.path.join(script_path, 'LastCommand.txt')

		with open(last_command_path, "w") as text_file:
			text_file.write(last_command)
	
		text_file.close()
	
	def parse_argv(self, argv):
		
		executable_args = [	'--no-plots', '--overwrite', 
							'--corr none', '--no-verify', '--match none', 
							'--rdls none', '--new-fits none',
							'--index-xyls none', '--crpix-center' ]
		filename = None
		
		if self.__custom_L_enable:
			executable_args.append('-L ' + self.__custom_L)
			
		if self.__custom_H_enable:
			executable_args.append('-H ' + self.__custom_H)
		
		if self.__custom_objs_enable:
			executable_args.append('--objs' + self.__custom_objs)

		try:
			opts, args = getopt.getopt(	argv,
										self.__solve_fields_sargs,
										self.__solve_fields_largs
			)
														
		except getopt.GetoptError as e:
			print(e)
			self.write_last_command(str(e))
			self.help()
			sys.exit(2)

		for opt, arg in opts:
						
			if opt in ("-h", "--help"):
				executable_args.append('-h')
			elif opt in ("-u", "--scale-units"):
				executable_args.append('-u ' + arg)
			elif opt in ("-L", "--scale-low") and not self.__custom_L_enable:
				executable_args.append('-L ' + arg)
			elif opt in ("-H", "--scale-high") and not self.__custom_H_enable:
				executable_args.append('-H ' + arg)
			elif opt in ("-z", "--downsample"):
				executable_args.append('-z ' + arg)
			elif opt in ("-b", "--backend-config"):
				executable_args.append('-b ' + arg)
			elif opt in ("-W", "--wcs"):
				executable_args.append('-W ' + arg)
			elif opt in ("-k", "--keep-xylist"):
				executable_args.append('-k ' + arg)
			elif opt in ("--objs") and not self.__custom_objs_enable:
				executable_args.append('--objs ' + arg)
			elif opt in ("-C", "--cancel"):
				executable_args.append('-C ' + arg)
				
			argv.remove(opt)
			if arg:
				argv.remove(arg)
				
				
		if len(argv) != 1:
			print("Invalid arguments")
			sys.exit(2)

		# Filename
		executable_args.append(argv[0])
		
		# Command Line
		cmd_line = self.__solve_field_bin + ' ' + ' '.join(executable_args)
		
		self.write_last_command(cmd_line)
		
		# Execute solve-field
		subprocess.run(cmd_line, shell=True)

	
def main(argv):
	solve_field_fallback = SolveFieldFallback()
	solve_field_fallback.parse_argv(argv)
	
if __name__ == "__main__":
   main(sys.argv[1:])	


	
