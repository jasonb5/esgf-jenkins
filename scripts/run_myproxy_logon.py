import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from MiscUtil import *

parser = argparse.ArgumentParser(description="run esgf 2.x post install steps",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-f", "--vars_file",
                    help='ansible host var file')
parser.add_argument("-x", "--index_idp_node",
                    help='index_idp_node')

args = parser.parse_args()
vars_file = args.vars_file
index_idp_node = args.index_idp_node

# get admin_pass 
admin_pass = get_var_val(vars_file, 'admin_pass')
print("DEBUG...get_var_val returned: {v}".format(v=admin_pass))

myproxy_logon_exp = os.path.join(this_dir, 'myproxy_logon.exp')

update_file(myproxy_logon_exp, 'INDEX_IDP_NODE', index_idp_node, workdir)
update_file(myproxy_logon_exp, 'MYPROXY_PASS', admin_pass)

cmd = myproxy_logon_exp
conda_path = "/usr/local/conda/bin"
status = run_in_conda_env_as_root(conda_path, 'esgf-pub', cmd)

sys.exit(status)
