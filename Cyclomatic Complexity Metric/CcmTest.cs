namespace CcmTest
{
    class Program
    {
        static void Main(string[] args)
        {
            if (c1())
                f1();
            else
                f2();

            if (c2())
                f3();
            else
                f4();
			
			StronglyConnected();
        }
		
        public static bool c1() { return true }
        public static bool c2() { return false }

        public static void f1() { }
        public static void f2() { }
        public static void f3() { }
        public static void f4() { }
		
        public static void StronglyConnected()
        {
			do {
				if (c1())
					f1();
				else
					f2();

				if (c2())
					f3();
				else
					f4();
			}
			while(true)
        }
    }
}