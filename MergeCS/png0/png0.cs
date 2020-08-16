using ImageMagick;
using System;
using System.Collections.Concurrent;
using System.IO;
namespace WMD
{
    namespace png0
    {
        class png0
        {
            static void Main(string[] args)
            {
                ConcurrentQueue<worker.WorkItem> q = new ConcurrentQueue<worker.WorkItem>();
                string[] files = Directory.GetFiles("png0");
                foreach (string theFile in files)
                {
                    q.Enqueue(new worker.WorkItem { Name = theFile, IsFile = true });
                }
                worker.worker.work(5, delegate () { Task(q); });
            }
            static void Task(ConcurrentQueue<worker.WorkItem> q)
            {
                worker.WorkItem workItem;
                while (q.Count != 0 && q.TryDequeue(out workItem))
                {
                    if (workItem.IsFile)
                    {
                        using (MagickImage image = new MagickImage(workItem.Name))
                        {
                            string temp = "resultPng0/" + Path.GetFileName(workItem.Name);
                            image.Quality = 100;
                            image.Write(temp);
                            Console.WriteLine(temp);
                        }
                    }
                }
            }
        }
    }
}

