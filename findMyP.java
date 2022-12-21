package mypkg;

public class findMyP {

	public static void main(String[] args) {
		double domain = findDomain(360);
		System.out.println("Found Domain. our P is between "+(domain-200)+" and "+domain);
		double P = findP(domain-200,domain);
		System.out.println("Found P. our P is "+P);
	}
	public static double findDomain(int x) {
		for(int i = 1 ;i<50 ; i++) {
			double p = i*200;
			double S=250000;
			for(int j = 1 ; j<=360 ;j++) {
				double cache=S+(0.004*S)-p;
				S=cache;
				System.out.println("Running findDomain: Checking for p="+p+": After "+j+" Months, S is "+S);
				if (S<=0)return p;
			}

		}
		return 9999999.0;
	}
	
	public static double findP(double start,double end) {
		if (start==end)return start;
		double mid = start + (end - start) / 2;
		if (start==mid || end==mid)return mid;
		double S=250000;
		for(int j = 1 ; j<=360 ;j++) {
			double cache=S+(0.004*S)-mid;
			S=cache;
			System.out.println("Running findP: Checking for p="+mid+": After "+j+" Months,Start="+start+" End="+end+" S is "+S);
			if (S<=0) {if(S==0 && j==360)return mid;else return findP(start,mid);}
		}
		return findP(mid,end);
	}
}
