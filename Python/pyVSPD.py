"""
pyVSPD
======

Interface to work with vSPD from python without having to manually
edit and mung GAMS files
"""

import os
import subprocess

class GDXModifier(object):
    """GDXModifier"""

    GAMS_Folder = '/home/nigel/Gams/24.1/'
    gdxdump = os.path.join(GAMS_Folder, "gdxdump")
    gams = os.path.join(GAMS_Folder, 'gams')
    input_dir = "/home/nigel/python/vSPD/Input"

    def __init__(self, gdx_file):
        super(GDXModifier, self).__init__()
        self.gdx = gdx_file

    def gdx_to_gams(self):

        fName, ext = os.path.splitext(self.gdx)
        cwd = os.getcwd()
        abs_fName = os.path.join(self.input_dir, self.gdx)
        gms_fName = os.path.join(cwd, fName) + '.gms'
        output = "Output=%s" % gms_fName
        subprocess.call(['wine', self.gdxdump, abs_fName, output])

        self.gms = gms_fName



    def tidy_up(self):
        """ Tidy up the Python directory and make sure only the
        appropriate files are in the input directory
        """

    def single_period_gms(self, trading_period):

        # Make sure TP is in the trading period
        if "TP" not in str(trading_period):
            trading_period = "TP%s" % trading_period

        # Add the data to a list
        with open(self.gms, 'r') as f:
            gms_data = [line for line in f]
        
        scrubbed_gms_data = []

        # Iterate through the data and apply classifiers:
        for i, line in enumerate(gms_data):
            try:
                future_line = gms_data[i+1]
            except:
                future_line = None

            param_type = line.split(' ')
            if param_type[0] in ("Set", "Parameter"):
                check_flag = True

            if line[1:3] != "TP":
                scrubbed_gms_data.append(line)

            elif trading_period in line[1:5]:

                if check_flag and trading_period not in future_line[1:5]:
                    line = line[:-4] + ' /;\n'
                    check_flag = False
                scrubbed_gms_data.append(line)

        self.scrubbed_gms_data = scrubbed_gms_data
        scrub_name, ext = os.path.splitext(self.gms)
        scrub_name = scrub_name + str(trading_period[2:]) + ext

        with open(scrub_name, 'wb') as f:
            for line in scrubbed_gms_data:
                f.write("%s" % line)

        self.scrub_name = scrub_name


    def gms_to_gdx(self):
        """
        Note Gams will shut itself with absolute file names.
        Need to run with relative ones.
        """

        cwd = os.getcwd()
        scrub_name = os.path.basename(self.scrub_name)
        gdx_name, ext  = os.path.splitext(scrub_name)
        
        gdx_name += '.gdx'
        out = "gdx=%s" % gdx_name
        cmd = ['wine', self.gams, scrub_name, out]
        subprocess.call(cmd)


    def modify_hvdc(self):
        pass
