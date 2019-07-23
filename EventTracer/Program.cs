using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Microsoft.Diagnostics.Symbols;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.Kernel;

namespace EventTracer
{
    class Program
    {
        static void Main(string[] args)
        {
            //Check admin privileges
            if(TraceEventSession.IsElevated() == false)
            {
                Console.WriteLine("Please run me as Administrator");
                return;
            }

           //Initializing ETW session
           using (var kernelSession = new TraceEventSession("ChaChaRealSmooth"))
            {
                Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e) { kernelSession.Dispose(); };

                //subscribe to kernel events
                kernelSession.EnableKernelProvider(
                    KernelTraceEventParser.Keywords.ImageLoad | //dll loads
                    KernelTraceEventParser.Keywords.Process     //start/stop porcess
                );

                //Setup function handlers
                kernelSession.Source.Kernel.ImageLoad += dllLoaded;
                kernelSession.Source.Kernel.ProcessStart += processStarted;
                kernelSession.Source.Kernel.ProcessStop += processStopped;

                kernelSession.Source.Process();
            }
        }

        private static void dllLoaded(ImageLoadTraceData data)
        {
            Console.WriteLine("DLL loaded: {0}\n\tby process: {1}\n\tfor an operation: {2}\n\tusing the processor: {3}\n\tprovider: {4}\n\tLoaded by thread: {5}\n\n", data.FileName, data.ProcessID, data.Opcode, data.ProcessorNumber, data.ProviderGuid, data.ThreadID);
        }

        private static void processStarted(ProcessTraceData data) { }

        private static void processStopped(ProcessTraceData data) { }

    }
}
