package wikiServerSim;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.cloudbus.cloudsim.Host;
import org.cloudbus.cloudsim.Log;
import org.cloudbus.cloudsim.Vm;
import org.cloudbus.cloudsim.VmAllocationPolicy;
import org.cloudbus.cloudsim.core.CloudSim;

class StaticRandomVmAllocationPolicy extends VmAllocationPolicy{

	private final Map<String, Host> vm_table = new HashMap<String, Host>();
	private final List<Host> hosts;

	@SuppressWarnings("unchecked")
	public StaticRandomVmAllocationPolicy(List<? extends Host> list) {
		super(list);
		this.hosts = (List<Host>) list;
	}

	
	@Override
	public boolean allocateHostForVm(Vm vm) {
		if(this.vm_table.containsKey(vm.getUid()))
			return true;
		
		// otherwise,
		while (true){
			Host assigned = hosts.get(new Random().nextInt(hosts.size()));
			if (this.allocateHostForVm(vm, assigned))
				return true;
		}
	}

	@Override
	public boolean allocateHostForVm(Vm vm, Host host) {
		if (host != null && host.vmCreate(vm)){
			vm_table.put(vm.getUid(), host);
			Log.formatLine("%.4f: VM #" + vm.getId() + " has been allocated to the host#" + host.getId() + 
					" datacenter #" + host.getDatacenter().getId() + "(" + host.getDatacenter().getName() + ") #", 
					CloudSim.clock());
			return true;
		}
		return false;
	}

	@Override
	public void deallocateHostForVm(Vm vm) {
		Host host = this.vm_table.remove(vm.getUid());
		
		if (host != null)
			host.vmDestroy(vm);
	}

	@Override
	public Host getHost(Vm vm) {
		return this.vm_table.get(vm.getUid());
	}

	@Override
	public Host getHost(int vmId, int userId) {
		return this.vm_table.get(Vm.getUid(userId, vmId));
	}

	@Override
	public List<Map<String, Object>> optimizeAllocation(List<? extends Vm> vmList) {
		// TODO Auto-generated method stub
		return null;
	}
	
}