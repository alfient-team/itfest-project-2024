// reason of do not implementing interface, concrete class
// this service here is going to have to run the background
// it's going to we're going to start it when our service starts
// and it's going to be Continuously listening on our message bus
// for events and because of that we have to build it in a slighty different way
// we don't use the interface, concrete class, repository (it is some torturous)
// we are building basically something called Background service
using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using CommandsService.EventProcessing;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace CommandsService.AsyncDataServices
{
    // MessageBusSubscriber will run EventProcessor
    // as in a Singleton lifetime
    // and as Background Service
    public class MessageBusSubscriber : BackgroundService
    {
        private readonly IConfiguration _configuration;
        private readonly IEventProcessor _eventProcessor;
        private IConnection _connection;
        private IModel _channel;
        private string _queueName;

        public MessageBusSubscriber(
            IConfiguration configuration,
            IEventProcessor eventProcessor
        )
        {
            _configuration = configuration;
            _eventProcessor = eventProcessor;

            InitializeRabbitMQ();
        }

        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            stoppingToken.ThrowIfCancellationRequested();

            var consumer = new EventingBasicConsumer(_channel);

            consumer.Received += (ModuleHandle, ea) =>
            {
                Console.WriteLine("--> Event Received!");

                var bodyMsg = ea.Body;
                var notificationMessage = Encoding.UTF8.GetString(bodyMsg.ToArray());

                _eventProcessor.ProcessEvent(notificationMessage);
            };

            _channel.BasicConsume(
                queue: _queueName,
                autoAck: true,
                consumer: consumer
            );

            return Task.CompletedTask;
        }

        private void InitializeRabbitMQ()
        {
            // RabbitMQ Connection Factory
            var factory = new ConnectionFactory() {
                HostName = _configuration["RabbitMQHost"],
                Port = int.Parse(_configuration["RabbitMQPort"])
            };

            try
            {
                _connection = factory.CreateConnection();
                _channel = _connection.CreateModel();

                _channel.ExchangeDeclare(exchange: "trigger", type: ExchangeType.Fanout);

                // for listener (to listen)
                _queueName = _channel.QueueDeclare().QueueName;
                _channel.QueueBind(
                    queue: _queueName,
                    exchange: "trigger",
                    routingKey: ""
                );
                Console.WriteLine("--> Connected and Listening on the Message Bus...");

                _connection.ConnectionShutdown += RabbitMQ_ConnectionShutdown;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"--> Could not connect to the Message Bus and Listen it {ex.Message}");
            }
        }

        private void RabbitMQ_ConnectionShutdown(object sender, ShutdownEventArgs e)
        {
            Console.WriteLine("--> RabbitMQ Connection Shutdown");
        }

        public override void Dispose()
        {
            if (_channel.IsOpen)
            {
                _channel.Close();
                _connection.Close();
            }

            base.Dispose();
        }
    }
}