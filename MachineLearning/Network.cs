using System;
using NeuralNetworkNET;
using NeuralNetworkNET.SupervisedLearning;
using System.Threading.Tasks;
using NeuralNetworkNET.APIs;
using NeuralNetworkNET.APIs.Datasets;
using NeuralNetworkNET.APIs.Enums;
using NeuralNetworkNET.APIs.Interfaces;
using NeuralNetworkNET.APIs.Interfaces.Data;
using NeuralNetworkNET.APIs.Results;
using NeuralNetworkNET.APIs.Structs;
using NeuralNetworkNET.Helpers;
using NeuralNetworkNET.SupervisedLearning.Progress;
using NeuralNetworkNET.Networks;
using NeuralNetworkNET.Networks.Graph;
using NeuralNetworkNET.Networks.Activations;


namespace MachineLearning
{
    class NNetwork
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            INeuralNetwork network = NetworkManager.NewGraph(TensorInfo.Linear(5), root =>
                var input1 = root.Layer(CuDnnNetworkLayers.FullyConnected
            );
        }
    }
}
