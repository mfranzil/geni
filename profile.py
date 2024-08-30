import geni.portal as portal
import geni.rspec.pg as rspec
import os

# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter("n", "Number of VMs", portal.ParameterType.INTEGER, 2)

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Check parameter validity.
if params.n < 1 or params.n > 8:
    portal.context.reportError(portal.ParameterError("You must choose at least 1 and no more than 100 VMs.", ["n"]))

# Abort execution if there are any errors, and report them.
portal.context.verifyParameters()

for i in range(params.n):
    # Create a XenVM and add it to the RSpec.
    node = request.XenVM("node_" + str(i))
    node.cores = 4
    node.ram = 4096
    # node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
    # node.addService(rspec.Install(url="http://example.org/sample.tar.gz", path="/local"))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh"))

    # Fetch the hostname and match it to a local file that maps node_n to a public key
    hostname = "node_" + str(i)
    key_file_path = "/local/repository/keys/" + str(hostname) + ".pub"
    
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as key_file:
            public_key = key_file.read().strip()
            node.addService(rspec.Execute(shell="bash", command="echo " + public_key + " >> /home/ubuntu/.ssh/authorized_keys"))
        
        # Delete the key file after adding the public key
        os.remove(key_file_path)

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()