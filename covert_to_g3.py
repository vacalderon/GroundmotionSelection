
import pandas as pd
import os

# Mainshock and Aftershock Paths

MS_path= r'C:\ConditionDependentPBEE\GroundMotion_Mainshock_Records'
MSListing = os.listdir(MS_path)
output_dir = r'C:\ConditionDependentPBEE\GroundmotionSelection\Response Spectrum Analysis\Mainshocks_RS'

for i in MSListing:
    with open(MS_path+"\\"+i) as GM1:
        head1 = [next(GM1) for x in range(4)]
        Data1 = GM1.read()
        GM1.close

    a1 = Data1.split()
    A1 = [float(i) for i in a1]

    outputfile=output_dir+"\\"+i

    with open(outputfile, 'w') as f:
        for item in A1:
            f.write("%s\n" % item)