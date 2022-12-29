public class Mycache {

	public static void main(String[] args) {
		double MS = meanScore(1000);
		System.out.println("Mean score for n=1000 is:"+MS+" and for each dart is:"+(MS/5.0));
	}
	
	public static double meanScore(int n) {
		double totalScore = 0;
		for(int i = 0;i<n;i++) {
			double score = 0;
			for(int j = 0;j<5;j++) {
				double luck = Math.random();
				if(luck<=0.00545)score+=50.0;
				else if(luck<=0.03409)score+=25.0;
				else if(luck<=0.13635)score+=15.0;
				else if(luck<=0.34907)score+=10.0;
				else if(luck<=0.7854)score+=5.0;
				//else its missed.
			}
			totalScore=totalScore+score;
		}
		return totalScore/n;
	}
