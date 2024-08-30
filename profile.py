"""
A profile with a configurable number of nodes that runs a Postgres database on each node.

Instructions:
1. Run the profile.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

imageList = [
    ('default', 'Default Image'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD', 'UBUNTU 22.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS8S-64-STD',  'CENTOS 8 Stream'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD123-64-STD', 'FreeBSD 12.3'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD131-64-STD', 'FreeBSD 13.1')]

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList,
                   longDescription="Most clusters have this set of images, " +
                   "pick your favorite one.")

# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Optional physical node type",
                   portal.ParameterType.NODETYPE, "d820",
                   longDescription="Pick a single physical node type (pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")

# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter("n", "Number of nodes", portal.ParameterType.INTEGER, 1,
                                 longDescription="Choose the number of nodes to allocate. 1-8 nodes are allowed.")

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
    node.hardware_type = params.phystype
    node.disk_image = params.osImage
    # node = request.XenVM("node_" + str(i))
    # node.cores = 4
    # node.ram = 4096
    # node.addService(rspec.Install(url="http://example.org/sample.tar.gz", path="/local"))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()