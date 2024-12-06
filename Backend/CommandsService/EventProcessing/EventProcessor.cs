using System;
using System.Text.Json;
using System.Threading.Tasks.Dataflow;
using AutoMapper;
using CommandsService.Data;
using CommandsService.Dtos;
using CommandsService.Models;
using Microsoft.Extensions.DependencyInjection;

namespace CommandsService.EventProcessing
{
    enum EventType
    {
        PlatformPublished,  // CreatePlatform() in PlatformService
        Undetermined
    }

    public class EventProcessor : IEventProcessor
    {
        private readonly IServiceScopeFactory _scopeFactory;
        private readonly IMapper _mapper;

        public EventProcessor(
            IServiceScopeFactory scopeFactory,
            IMapper mapper
        )
        {
            _scopeFactory = scopeFactory;
            _mapper = mapper;
        }

        public void ProcessEvent(string message)
        {
            var eventType = DetermineEvent(message);

            switch (eventType)
            {
                case EventType.PlatformPublished:
                    AddPlatform(message);
                    break;
                default:
                    break;
            }
        }

        private void AddPlatform(string platformPublishedMessage)
        {
            using (var scope = _scopeFactory.CreateScope())
            {
                // variable to contain repository
                // get reference
                // as opposed to injecting it through constructive dependency
                // lifetime of repository
                var repo = scope.ServiceProvider.GetRequiredService<ICommandRepo>();

                // deserialize string platformPublishedMessage
                // into proper PlatformPublishedDto
                var platformPublishedDto = JsonSerializer.Deserialize<PlatformPublishedDto>(platformPublishedMessage);

                try
                {
                    var plat = _mapper.Map<Platform>(platformPublishedDto);
                    if (!repo.ExternalPlatformExists(plat.ExternalId))
                    {
                        repo.CreatePlatform(plat);
                        repo.SaveChanges();

                        Console.WriteLine("--> Platform was created succesfully");
                    }
                    else
                    {
                        Console.WriteLine("--> Platform already exists...");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"--> Could not add Platform to DB {ex.Message}");
                    throw;
                }
            }
        }

        private EventType DetermineEvent(string notificationMessage)
        {
            Console.WriteLine("--> Determining Event...");

            var eventType = JsonSerializer.Deserialize<GenericEventDto>(notificationMessage);

            switch (eventType.Event)
            {
                // TODO: make this Event msg (of determination) "Platform_Published"
                // constant type and include it in configs.json (store it in config file)
                case "Platform_Published":
                    Console.WriteLine("--> Platform Published Event Detected (EventType.PlatformPublished)");
                    return EventType.PlatformPublished;
                default:
                    Console.WriteLine("--> Could not determine the Event type (EventType.Undetermined)");
                    return EventType.Undetermined;
            }
        }
    }
}