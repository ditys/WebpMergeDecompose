using System;
using System.Threading;
using ImageMagick;

namespace WMD
{
    namespace worker
    {
        public struct WorkItem
        {
            public string Name;
            public bool IsFile;
        }
        public class worker
        {
            public static void work(int threadNumbers, Action a)
            {
                Thread[] Threads = new Thread[threadNumbers];
                try
                {
                    for (int i = 0; i < threadNumbers; i++)
                    {
                        Threads[i] = new Thread(new ThreadStart(delegate ()
                        {
                            a.Invoke();
                        }));
                        Threads[i].Start();
                    }
                    for (int i = 0; i < threadNumbers; i++)
                    {
                        Threads[i].Join();
                    }
                }
                catch (MagickException e)
                {
                    Console.WriteLine(e.ToString());
                }
            }
        }
    }
}
