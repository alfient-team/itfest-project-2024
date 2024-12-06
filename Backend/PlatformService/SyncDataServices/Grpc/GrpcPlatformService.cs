using System;
using System.Threading.Tasks;
using AutoMapper;
using Grpc.Core;
using PlatformService.Data;

namespace PlatformService.SyncDataServices.Grpc
{
    // generated code via protoc (in \Debug\Protos\...)
    // inheritance by service GrpcPlatform in \Protos\platforms.proto file
    public class GrpcPlatformService : GrpcPlatform.GrpcPlatformBase
    {
        private readonly IPlatformRepo _repository;
        private readonly IMapper _mapper;

        public GrpcPlatformService(IPlatformRepo repository, IMapper mapper)
        {
            _repository = repository;
            _mapper = mapper;
        }

        public override Task<PlatformResponse> GetAllPlatforms(
            GetAllRequest request,
            ServerCallContext context
        )
        {
            var response = new PlatformResponse();
            var platforms = _repository.GetAllPlatforms();

            Console.WriteLine("--> gRPC call was successfully hitted by Client in the Server");
            foreach (var plat in platforms)
            {
                response.Platform.Add(_mapper.Map<GrpcPlatformModel>(plat));
            }

            return Task.FromResult(response);
        }
    }
}