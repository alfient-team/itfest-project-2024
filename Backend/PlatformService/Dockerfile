#FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build-env
#WORKDIR /app

#COPY *.csproj ./
#RUN dotnet restore

#COPY . ./
#RUN dotnet publish -c Release -o out

## make image smaller with build-env sdk
## runtime image
#FROM mcr.microsoft.com/dotnet/aspnet:5.0
#WORKDIR /app
#COPY --from=build-env /app/out .

#ENTRYPOINT [ "dotnet" "PlatformService.dll" ]

FROM mcr.microsoft.com/dotnet/aspnet:5.0 as base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
COPY . /src
WORKDIR /src
RUN ls
RUN dotnet build "PlatformService.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "PlatformService.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "PlatformService.dll"]
