import glob2, os
def build_vrt(string):
    flist = glob2.glob(f'**/*{string}*.tif')
    l = ' '.join(flist)
    print(f"Running {string}. {len(flist)} files")
    s = f'gdalbuildvrt {string}.vrt {l}'
    os.system(s)
	
def main():
    for s in ['rgb', 'nir']:
        
        try:
            build_vrt(s)
        except:
            continue
			
if __name__ == '__main__':
	main()