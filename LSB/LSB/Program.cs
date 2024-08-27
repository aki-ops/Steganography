using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Reflection;
using System.Text;
using ColorMine.ColorSpaces;
using ColorMine.ColorSpaces.Comparisons;

class Program
{
    //Embed the message in the first 2 bits of the pixel
    public static void Stego(int index, string mess, ref int[,] stoArray)
    {
        Console.Write(stoArray[index, 2] + " " + mess[0] + " " + stoArray[index, 3] + " " + mess[1] + " " + stoArray[index, 4] + " " + mess[2]);
        stoArray[index, 2] &= 254;
        stoArray[index, 3] &= 254;
        stoArray[index, 4] &= 254;

        stoArray[index, 2] += Convert.ToInt32(mess.Substring(0, 1), 2);
        stoArray[index, 3] += Convert.ToInt32(mess.Substring(1, 1), 2);
        stoArray[index, 4] += Convert.ToInt32(mess.Substring(2, 1), 2);
        Console.WriteLine(" " + stoArray[index, 2] + " " + stoArray[index, 3] + " " + stoArray[index, 4]);
    }

    public static string Decrypt(int[,] StoArray)
    {
        StringBuilder len = new StringBuilder();
        //Console.WriteLine(StoArray[1, 0]);
        for (int i = 0; i <= 3; i++)
        {
            len.Append(Convert.ToString(StoArray[i, 0] - (StoArray[i, 0] & 254), 2).PadLeft(1, '0'));
            len.Append(Convert.ToString(StoArray[i, 1] - (StoArray[i, 1] & 254), 2).PadLeft(1, '0'));
            len.Append(Convert.ToString(StoArray[i, 2] - (StoArray[i, 2] & 254), 2).PadLeft(1, '0'));
        }
        int lenStego = Convert.ToInt32(len.ToString(), 2);

        StringBuilder mess = new StringBuilder();
        for (int i = 4; i < lenStego * 8 / 3 + 4 + 1; i++)
        {
            mess.Append(Convert.ToString(StoArray[i, 0] - (StoArray[i, 0] & 254), 2).PadLeft(1, '0'));
            mess.Append(Convert.ToString(StoArray[i, 1] - (StoArray[i, 1] & 254), 2).PadLeft(1, '0'));
            mess.Append(Convert.ToString(StoArray[i, 2] - (StoArray[i, 2] & 254), 2).PadLeft(1, '0'));
        }
        //Console.WriteLine(mess.ToString());
        return mess.ToString().Remove(0, (lenStego * 8 / 3 + 1) * 3 - lenStego * 8);
    }

    public static string BinaryToString(string data)
    {
        byte[] bytes = new byte[data.Length / 8];

        for (int i = 0; i < data.Length / 8; i++)
        {
            string binaryString = data.Substring(i * 8, 8);
            bytes[i] = Convert.ToByte(binaryString, 2);
        }

        string convertedString = Encoding.UTF8.GetString(bytes);
        return convertedString;
    }
    public static string StringToBinary(string data)
    {
        byte[] bytes = Encoding.UTF8.GetBytes(data);
        StringBuilder binary = new StringBuilder();

        foreach (byte b in bytes)
        {
            binary.Append(Convert.ToString(b, 2).PadLeft(8, '0'));
        }
        return binary.ToString();
    }

    public static void Main(string[] args)
    {
        Console.WriteLine("1. Hide information in photos");
        Console.WriteLine("2. Extract hidden information in images");
        Console.Write("Choose option: ");
        int ans = Convert.ToInt32(Console.ReadLine());

        if (ans == 1)
        {
            //Path to the cover image
            string imagePath = "image.png";
            Bitmap image = (Bitmap)Image.FromFile(imagePath);

            int width = image.Width;
            int height = image.Height;
            int index = 0;

            int[,] stoArray = new int[width * height, 5];

            for (int i = 0; i < width; i++)
            {
                for (int j = 0; j < height; j++)
                {
                    Color pixel = image.GetPixel(i, j);

                    stoArray[index, 0] = i;
                    stoArray[index, 1] = j;
                    stoArray[index, 2] = pixel.R;
                    stoArray[index, 3] = pixel.G;
                    stoArray[index, 4] = pixel.B;

                    index++;
                }
            }

            //Path to file secret message
            string messPath = "Import.txt";
            string mess = File.ReadAllText(messPath);

            mess = StringToBinary(mess);
            string steLenMess = Convert.ToString(mess.Length / 8, 2).PadLeft(12, '0');
            mess = mess.PadLeft((3 - (mess.Length % 3)) + mess.Length, '0');
            index = 0;
            double total = 0.0;
            for (int i = 0; i < steLenMess.Length; i += 3)
            {
                // Console.Write(StoArray[index, 2] + " " + StoArray[index, 3] + " " + StoArray[index, 4]);
                // var rgbColor1 = new Rgb { R = stoArray[index, 2], G = stoArray[index, 3], B = stoArray[index, 4] };

                Stego(index, steLenMess.Substring(i, 3), ref stoArray);

                var rgbColor2 = new Rgb { R = stoArray[index, 2], G = stoArray[index, 3], B = stoArray[index, 4] };


                // Convert from RGB to Lab color space
                //var labColor1 = rgbColor1.To<Lab>();
                //var labColor2 = rgbColor2.To<Lab>();

                // Calculate Delta E between two colors
                // total += labColor1.Compare(labColor2, new Cie1976Comparison());
                // Console.WriteLine(" " + $"Delta E between color1 and color2: {deltaE}");

                index++;
            }

            for (int i = 0; i < mess.Length; i += 3)
            {
                var rgbColor1 = new Rgb { R = stoArray[index, 2], G = stoArray[index, 3], B = stoArray[index, 4] };
                Stego(index, mess.Substring(i, 3), ref stoArray);
                var rgbColor2 = new Rgb { R = stoArray[index, 2], G = stoArray[index, 3], B = stoArray[index, 4] };
                var labColor1 = rgbColor1.To<Lab>();
                var labColor2 = labColor1.To<Lab>();
                total += labColor1.Compare(labColor2, new Cie1976Comparison());
                index++;
            }

            Bitmap newImage = new Bitmap(width, height, PixelFormat.Format24bppRgb);
            index = 0;

            for (int i = 0; i < width; i++)
            {
                for (int j = 0; j < height; j++)
                {
                    Color pixel = Color.FromArgb(stoArray[index, 2], stoArray[index, 3], stoArray[index, 4]);
                    newImage.SetPixel(i, j, pixel);
                    index++;
                }
            }

            //Path to file secret mess
            string outputPath = "stego_image.png";
            newImage.Save(outputPath, ImageFormat.Png);
        }



        else if (ans == 2)
        {
            // Path to stego image
            string stegoImage = "stego_new_image.png";
            Bitmap image = (Bitmap)Image.FromFile(stegoImage);

            int width = image.Width;
            int height = image.Height;
            int index = 0;

            int[,] stoArray = new int[width * height, 3];

            for (int i = 0; i < width; i++)
            {
                for (int j = 0; j < height; j++)
                {
                    Color pixel = image.GetPixel(i, j);

                    stoArray[index, 0] = pixel.R;
                    stoArray[index, 1] = pixel.G;
                    stoArray[index, 2] = pixel.B;

                    index++;
                }
            }

            string mess = Decrypt(stoArray);

            // Path to decrypted message txt
            string messPath = "Export.txt";
            File.WriteAllText(messPath, BinaryToString(mess));
        }


        else
        {
            Console.WriteLine("ERROR!!!");
        }
    }
}
