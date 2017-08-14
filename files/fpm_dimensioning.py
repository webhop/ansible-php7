#!/usr/bin/env python

'''
Set PHP-FPM pm.max_children in order to maximize usage of available memory in the box at startup time.

'''
import os
import logging
import argh
import fileinput
import re

LOGGER = logging.getLogger(__name__)

def get_php_fpm_memory(php_fpm_total_ram_slice=0.4):
    # Taken from http://stackoverflow.com/a/28161352
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
    mem_megs = mem_bytes/(1024.**2)  # e.g. 3.74
    LOGGER.info("Total memory available in the system: %sM", '%d' % mem_megs)

    return mem_megs * php_fpm_total_ram_slice

@argh.arg("--memratio", help="Slice or ratio of RAM allocated to PHP-FPM. 0 means no RAM, 1 means all the RAM available. Defaults to 0.4.", default=0.4)
@argh.arg("--confpath", help="Pool configuration file path. Defaults to /etc/php5/fpm/pool.d/www.conf.", default="/etc/php5/fpm/pool.d/www.conf")
@argh.arg("--avgmem", help="Estimated safe average memory per thread (in megs). Defaults to 128.", default=128)
def write_max_children_config(**kwargs):
    '''Overwrites the max children value in the default PHP-FPM config
    '''

    memratio = kwargs['memratio']
    confpath = kwargs['confpath']
    avgmem = kwargs['avgmem']
    
    LOGGER.info("Memory slice or ratio to be used by PHP-FPM is %s (%s%% of the total memory available.)", memratio, '%d' % (memratio * 100))
    LOGGER.info("Calculating max_children for a %sM (in average) memory footprint per thread...", avgmem)

    max_children = 5
    
    if avgmem > 0:
        max_children = get_php_fpm_memory(memratio) / avgmem
        if max_children < 5:
            LOGGER.warning("Calculated max_children value of %s is too low. Try to lower the PHP application's memory footprint, or consider adding more memory to the box.", '%d' % max_children)
    
    conf_file = fileinput.FileInput(confpath, inplace=True)
    LOGGER.info("Writing pm.max_children value of %s to %s...", '%d' % max_children, confpath)
    
    for line in conf_file:
        line = re.sub(r"^pm.max_children = .*$", 'pm.max_children = ' + '%d' % max_children + ' ;Modified by /opt/beamly/scripts/php/fpm_dimensioning.py (upstart)' , line.rstrip())
        print(line)
    LOGGER.info("Done dimensioning pm.max_children.")

if __name__ == "__main__":
    FORMAT = "%(asctime)-15s : %(levelname)-8s : %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    # overwrite config file
    argh.ArghParser()
    argh.dispatch_command(write_max_children_config)
