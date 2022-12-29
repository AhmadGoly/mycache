public class Mycache {

	public static void main(String[] args) {
		double hartime=0;double maxhar=0;double waittime=0;double maxwait=0;
		double idletime=0;double lastfinish=0;
		int n = 100;
		double[] between = new double[n];
		double[] arrive = new double[n];
		double[] unload = new double[n];
		double[] finish = new double[n];
		double[] idle = new double[n];
		double[] wait = new double[n];
		double[] start = new double[n];
		double[] harbor = new double[n];
		double timediff;
		between[1]=15+Math.random()*130;
		unload[1]=45+Math.random()*45;
		arrive[1]=between[1];
		hartime=unload[1];maxhar=unload[1];
		idletime=arrive[1];finish[1]=arrive[1]+unload[1];
		for(int i =2;i<n;i++) {
			between[i]=15+Math.random()*130;
			unload[i]=45+Math.random()*45;
			arrive[i]=arrive[i-1]+between[i];
			timediff=arrive[i]-finish[i-1];
			if(timediff>1) {
				
				idle[i]=timediff;
				wait[i]=0;
				
			}else {
				idle[i]=0;
				wait[i]=-timediff;
			}
			start[i]=arrive[i]+wait[i];
			finish[i]=start[i]+unload[i];
			harbor[i]=wait[i]+unload[i];
			
			hartime+=harbor[i];
			if(harbor[i]>maxhar) {
				maxhar=harbor[i];
			}
			waittime+=wait[i];
			idletime+=idle[i];
			
			if(wait[i]>maxwait) {
				maxwait=wait[i];
			}
			
			if(i==(n-1)) {
				lastfinish=finish[i];
			}
		}
		hartime=hartime/n;
		waittime=waittime/n;
		idletime=idletime/lastfinish;
		System.out.println("Running for n:"+n+"\nCalculated Hartime is:"+hartime+"\n
				   Calculated Wait time is:"+waittime+"\nCalculated Maxhar is:"+maxhar+"\n
				   Calculated Maxwait is:"+maxwait+"\nCalculated Idletime is:"+idletime);
	}
	

}
