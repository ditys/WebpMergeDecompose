using ImageMagick;
using System.Collections.Concurrent;

namespace Merge
{
	internal class Program
	{
		class ImageItem
		{
			public string imgName { get; set; }
			public bool isFile { get; set; }
		}
		static void Main(string[] args)
		{
			ConcurrentQueue<ImageItem> queue = new ConcurrentQueue<ImageItem>();
			if (!Directory.Exists("MergePhotos"))
			{
                Console.WriteLine("`MergePhotos` folder is not existed!");
				Console.ReadKey();
				return;
            }
			foreach (string item in Directory.GetFiles("MergePhotos"))
			{
				queue.Enqueue(new ImageItem { imgName = item, isFile = true });
			}
			foreach (string theFolder in Directory.GetDirectories("MergePhotos"))
			{
				queue.Enqueue(new ImageItem { imgName = theFolder, isFile = false });
			}
			Parallel.For(0, Environment.ProcessorCount, i =>
			{
				ImageItem item = new ImageItem { };
				while (queue.Count != 0 && queue.TryDequeue(out item))
				{
					if (item.isFile)
					{
						using (MagickImage image = new MagickImage(item.imgName))
						{
							string temp = "resultMerge/" + Path.GetFileName(item.imgName) + ".webp";
							image.Quality = 100;
							image.Write(temp);
							Console.WriteLine(temp);
						}
					}
					else
					{
						using (MagickImageCollection collection = new MagickImageCollection())
						{
							string[] mergeFiles = Directory.GetFiles(item.imgName);
							foreach (string f in mergeFiles)
							{
								collection.Add(f);
							}
							QuantizeSettings settings = new QuantizeSettings();
							settings.Colors = 256;
							collection.Quantize(settings);
							collection.Optimize();
							string temp = string.Format("resultMerge/{0}.webp", item.imgName.Substring(item.imgName.LastIndexOf('/') + 1));
							collection.Write(temp);
							Console.WriteLine(temp);
						}
					}
				}
			});
		}
	}

}