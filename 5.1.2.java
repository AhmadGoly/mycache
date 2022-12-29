public class Mycache {

	public static void main(String[] args) {
		int n = 100;
		int Counter=0;
		for (int i = 0;i<n;i++) {
			int timesBought=0;
			double x;
			double y;
			while(true) {
				timesBought++;
				x=Math.random();
				y=Math.random();
				if(x<=0.05 && y<=0.02)break;
			}
			//System.out.print(timesBought+" ");
			Counter=Counter+timesBought;
		}
		System.out.print("\n"+Counter/n);
	}

}
