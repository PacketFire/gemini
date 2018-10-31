
Vagrant.configure("2") do |config|
  config.vm.box = "debian/stretch64"

  config.vm.provision "shell", path: "provision.sh"

  config.vm.define "cephus" do |machine|
    machine.vm.hostname = "cephus"
  end

  config.vm.define "taurus" do |machine|
    machine.vm.hostname = "taurus"
  end
end
