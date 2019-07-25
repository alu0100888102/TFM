using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Microsoft.Diagnostics.Symbols;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.Kernel;
using System.Threading;
using System.IO;

namespace EventTracer
{
    class Tracingfromfile
    {
        static List<int> tracking;
        static TraceEventSession kernelSession;
        static Process baseProcess;


        static void Main(string[] args)
        {
            //Check admin privileges
            if (TraceEventSession.IsElevated() == false)
            {
                Console.WriteLine("Please run me as Administrator");
                return;
            }
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.InitialDirectory = "c:\\";
                openFileDialog.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
                openFileDialog.FilterIndex = 2;
                openFileDialog.RestoreDirectory = true;

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    //Get the path of specified file
                    filePath = openFileDialog.FileName;

                    //Read the contents of the file into a stream
                    var fileStream = openFileDialog.OpenFile();

                    using (StreamReader reader = new StreamReader(fileStream))
                    {
                        fileContent = reader.ReadToEnd();
                    }
                }
            }

            Tracingfromfile tracer = new Tracingfromfile("E:\\Games\\League of Legends\\LeagueClient.exe");
            tracer.begin();
        }

        public Tracingfromfile(string filename)
        {

            tracking = new List<int>();

            //Initializing ETW session
            kernelSession = new TraceEventSession("ChaChaRealSmooth");
            Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e) { kernelSession.Dispose(); };

            //subscribe to kernel events
            kernelSession.EnableKernelProvider(
            KernelTraceEventParser.Keywords.SystemCall | //dll loads
            KernelTraceEventParser.Keywords.Process     //start/stop porcess
            );

            //Setup function handlers
            kernelSession.Source.Kernel.PerfInfoSysClEnter += sysclenter;
            kernelSession.Source.Kernel.PerfInfoSysClExit += sysclexit;
            kernelSession.Source.Kernel.ProcessStart += processStarted;
            kernelSession.Source.Kernel.ProcessStop += processStopped;

            //setting up the staring process
            baseProcess = new Process();
            baseProcess.StartInfo.UseShellExecute = true;
            baseProcess.StartInfo.FileName = filename;
            baseProcess.StartInfo.CreateNoWindow = false;
        }

        public void begin()
        {
           
            try
            {
                ThreadStart ths = new ThreadStart(() => {
                    Thread.Sleep(2000);
                    baseProcess.Start();
                    Tracingfromfile.tracking.Add(baseProcess.Id);});
                Thread th = new Thread(ths);
                th.Start();
                kernelSession.Source.Process();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }


        private static void sysclenter (SysCallEnterTraceData data)
        {
            //if (Tracingfromfile.tracking.Contains(data.ProcessID))
            //if (data.EventName != "PerfInfo/SysClEnter")
            //Console.WriteLine("System call enter: {0}\n\tby process: {1}\n{2}\n", data.SysCallAddress, data.ProcessID, data.Dump());
            //File.AppendAllText(@"C:\\Users\\Ángel\\Desktop\\dumpfile.txt", "System call enter: "+ data.SysCallAddress + "\n\tby process: "+ data.ProcessID + "\n"+ data.Dump() + "\n");
        }
        private static void sysclexit(SysCallExitTraceData data)
        {
            //if (Tracingfromfile.tracking.Contains(data.ProcessID))
            //if(data.ProcessID != -1)
                //Console.WriteLine("System call exited: {0}\n\tby process: {1}\n\tpayload: {2}", data.SysCallNtStatus, data.ProcessID, data.Dump());
        }

        private static void processStarted(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
                Console.WriteLine("Process started ID: {0}\n{1}\n{2}\n\n", data.ProcessID, data.ImageFileName, data.ParentID);
            else if (Tracingfromfile.tracking.Contains(data.ParentID))
            {
                Tracingfromfile.tracking.Add(data.ProcessID);
                Console.WriteLine("Process started ID: {0}\n{1}\n{2}\n\n", data.ProcessID, data.ImageFileName, data.ParentID);
            }

        }

        private static void processStopped(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                Console.WriteLine("Process stopped ID: {0}\n{1}\n{2}\n\n", data.ProcessID, data.ImageFileName, data.ParentID);
                Tracingfromfile.tracking.Remove(data.ProcessID);
                if (Tracingfromfile.tracking.Count() == 0)
                    Console.WriteLine("The tree has ended");
            }
        }

    }
}
