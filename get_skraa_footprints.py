# data downloaded from 
# ftp://ftp.kortforsyningen.dk/grundlaeggende_landkortdata/skraafoto/Oblique_2019_footprints_27112019.zip
# to c:\Data\exdata
import os
import geopandas as gpd 


def run_cmd(cmd):
    """ run command line """
    print('CMD:', cmd)
    os.system(cmd)


def main(data_path, zipfile, csvfile, shpfile):
    """ major control flow """
    zipfile = os.path.join(data_path, zipfile)
    csvfile = os.path.join(data_path, csvfile)
    
    run_cmd('unzip {}'.format(zipfile))
    footprints = gpd.read_file(shpfile)
    print('crs initially:', footprints.crs) #epsg:25832
    footprints = footprints.to_crs({'init':'epsg:4326'}) # FutureWarning: '+init=<authority>:<code>' syntax is deprecated. '<authority>:<code>' is the preferred initialization method
    footprints["utc_day"] = footprints["timeutc"].str[:10]
    print(footprints.columns)
    print(footprints.head())
    footprints.to_csv(csvfile, sep=';')
    days = footprints["utc_day"].unique()
    with open(csvfile.replace('.csv', '.txt'), 'w') as w:
        for d in days:
            w.write('{}\n'.format(d))
    run_cmd("gzip {}".format(csvfile))

        
if __name__ == '__main__':
    data_path = '/mnt/exdata/' # r'c:\Data\exdata'
    zipfile   = 'Oblique_2019_footprints_27112019.zip'
    csvfile   = zipfile.replace('.zip', '.csv')
    shpfile   = 'footprints2019.shp'
    main( data_path, zipfile , csvfile, shpfile)
    
    
# run locally (on win)
# pip install geopandas
# python /mnt/code/get_skraa_footprints.py



