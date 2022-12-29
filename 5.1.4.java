public class Mycache {

	public static void main(String[] args) {
		int Counter = 0;
		int n = 100;
		for(int i =0;i<n;i++) {
			double x = Math.random()+0.5;
			double y = Math.random()*2;
			double real_y=Math.sqrt(x);
			if(y<=real_y)Counter++;
		}
		double Area=2*((double) Counter/n);
		System.out.println(Area);
	}

}
