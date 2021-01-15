
# author: Ingmar Nitze, ingmar.nitze@awi
# version: 0.2
# date: 2021-01-15

import glob2, os

def build_vrt(string):
    textfile = 'filelist.txt'
    flist = glob2.glob(f'**/*{string}*.tif')
    if len(flist) == 0:
        pass
    with open(textfile, 'w') as f:
        f.writelines("\n".join(flist))
    s = f'gdalbuildvrt -input_file_list {textfile} {string}.vrt'
    os.system(s)
    os.remove(textfile)
	
def main():
    for s in ['rgb', 'nir', 'dsm']:
        
        try:
            build_vrt(s)
        except:
            continue
			
if __name__ == '__main__':
	main()