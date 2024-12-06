using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using PlatformService.Dtos;

namespace PlatformService.SyncDataServices.Http
{
    public class HttpCommandDataClient : ICommandDataClient
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;

        // dependency injection
        public HttpCommandDataClient(HttpClient httpClient, IConfiguration configuration)
        {
            _httpClient = httpClient;
            _configuration = configuration;
        }

        public async Task SendPlatformToCommand(PlatformReadDto plat)
        {
            var httpContent = new StringContent(
                JsonSerializer.Serialize(plat),
                Encoding.UTF8,
                "application/json"
            );

            var requestURI = $"{_configuration["CommandService"]}";
            var response = await _httpClient.PostAsync(requestURI, httpContent);

            if (response.IsSuccessStatusCode)
            {
                Console.WriteLine($"--> Sync POST to CommandService was OK! with Id:{plat.Id}, Name:{plat.Name}");
            }
            else {
                Console.WriteLine("--> Sync POST to CommandService is NOT OK!");
            }
        }
    }
}