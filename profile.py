"""
A profile with a configurable number of VMs, each with 4 cores and 4GB of RAM, and a setup script that installs a public key for each VM and PostgreSQL.

Instructions:
1. Run the profile with the desired number of VMs.
3. Make changes to the setup.sh script as needed.
4. Run the profile.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter("n", "Number of nodes", portal.ParameterType.INTEGER, 1) 

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Check parameter validity.
if params.n < 1 or params.n > 8:
    portal.context.reportError(portal.ParameterError("You must choose at least 1 and no more than 8 nodes."))

# Abort execution if there are any errors, and report them.
portal.context.verifyParameters()

for i in range(params.n):
    # Create a XenVM and add it to the RSpec.
    node = request.RawPC("node" + str(i))
    # node = request.XenVM("node_" + str(i))
    # node.cores = 4
    # node.ram = 4096
    # node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
    # node.addService(rspec.Install(url="http://example.org/sample.tar.gz", path="/local"))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()