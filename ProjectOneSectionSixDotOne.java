package mypkg;

public class ProjectOneSectionSixDotOne {

	public static void main(String[] args) {
		double a = 1;
		double b = 0;
		boolean a_and_b_are_fixed=false;
		int N = 0;
		System.out.println("N		A		B		");
		System.out.println(N+"		"+a+"		"+b+"		");
		while(!a_and_b_are_fixed) {
			double cacheForA = (0.1*b)+(0.35*a);
			double cacheForB = (0.9*b)+(0.65*a);
			if(cacheForA==a && cacheForB==b) a_and_b_are_fixed=true;
			a = cacheForA;
			b = cacheForB;
			N++;
			System.out.println(N+"		"+a+"		"+b+"		");
		}

	}

}
