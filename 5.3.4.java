public class Mycache {

	public static void main(String[] args) {
		int [] Counter = new int [12]; //ma az Counter[0] estefade nemikonim. chon hichvaght A+B=1 nemishavad.
		int n = 10000000;
		System.out.println("running for n="+n);
		//Step 1:Use Monte Carlo:
		for(int i=0;i<n;i++) {
			int A; int B;
			double x=Math.random();
			if(x<=0.1)A=1;
			else if (x<=0.2)A=2;
			else if (x<=0.4)A=3;
			else if (x<=0.7)A=4;
			else if (x<=0.9)A=5;
			else A=6;
		
			double y=Math.random();
			if(y<=0.3)B=1;
			else if (y<=0.4)B=2;
			else if (y<=0.6)B=3;
			else if (y<=0.7)B=4;
			else if (y<=0.75)B=5;
			else B=6;
			
			Counter[A+B-1]++;
		}
		int cache=0;
		for(int i=0;i<12;i++) {
			System.out.println("probability of "+(i+1)+" is: "+(double)Counter[i]/n);
			cache=cache+Counter[i];
		}
		System.out.println("Count of all probabilities (Should be 1):"+(double)cache/n);
		
		//Step 2: Run 300 times with new probabilities.
		int count=0;
		for(int i = 0 ; i<300 ; i++) {
			double luck = Math.random();
			//sorry for bad if-else's. had no time to make it better.
			if(luck <=(double)Counter[1]/n)count=count+2;
			else if(luck <=(double)(Counter[1]+Counter[2])/n)count=count+3;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3])/n)count=count+4;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4])/n)count=count+5;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5])/n)count=count+6;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5]+Counter[6])/n)count=count+7;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5]+Counter[6]+Counter[7])/n)count=count+8;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5]+Counter[6]+Counter[7]+Counter[8])/n)count=count+9;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5]+Counter[6]+Counter[7]+Counter[8]+Counter[9])/n)count=count+10;
			else if(luck <=(double)(Counter[1]+Counter[2]+Counter[3]+Counter[4]+Counter[5]+Counter[6]+Counter[7]+Counter[8]+Counter[9]+Counter[10])/n)count=count+11;
			else count=count+12;
		}
		System.out.println("Sum of 300 rolls of two unfair dices calculated using new probabilities: "+count);
	}

}
