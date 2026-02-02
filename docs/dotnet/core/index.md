# AutoGen Core

AutoGen Core 的 .NET 版本沿用其 Python 版本的概念与约定。事实上，为了理解 .NET 版概念，我们建议先阅读 [Python 文档](https://microsoft.github.io/autogen/stable/)。除非另有说明，Python 版本中的概念可映射到 .NET。

语言版本之间的重要差异记录在 [与 Python 的差异](./differences-from-python.md) 中。仅影响特定语言的内容（如依赖注入或 Host Builder 模式）不会在差异文档中列出。

## 快速开始

你可以通过 NuGet 包获取 SDK，或克隆仓库。SDK 位于 [NuGet](https://www.nuget.org/packages/Microsoft.AutoGen)。
最低需要以下包：

```bash
dotnet add package Microsoft.AutoGen.Contracts
dotnet add package Microsoft.AutoGen.Core
```

更多安装说明见 [安装](./installation.md)。

你可以通过仓库 [samples](https://github.com/microsoft/autogen/tree/main/dotnet/samples) 目录快速上手。

### 创建一个 Agent

创建 agent 时，可以继承 BaseAgent 并实现关心事件的处理器。以下是最小示例，展示如何继承 BaseAgent 并实现事件处理器：

```csharp
public class MyAgent : BaseAgent, IHandle<MyMessage>
{
    // ...
    public async ValueTask HandleAsync(MyMessage item, MessageContext context)
    {
        // ...逻辑...
    }
}
```

通过继承 BaseAgent 可获得运行时与日志工具；通过实现 IHandle<T> 可为自定义消息定义事件处理方法。

### 在应用中运行 Agent

要在应用中运行 agent，可使用 `AgentsAppBuilder`。下面是运行名为 "HelloAgent" 的 agent 的示例：

```csharp
AgentsAppBuilder appBuilder = new AgentsAppBuilder()
    .UseInProcessRuntime(deliverToSelf: true)
    .AddAgent<HelloAgent>("HelloAgent");

var app = await appBuilder.BuildAsync();

// 通过向运行时发布消息来启动应用
await app.PublishMessageAsync(new NewMessageReceived
{
    Message = "Hello from .NET"
}, new TopicId("HelloTopic"));

// 等待关闭
await app.WaitForShutdownAsync();
```

## .NET SDK 运行时

.NET SDK 同时包含内存单进程运行时与远程分布式运行时，后者用于在云端运行 agents。分布式运行时支持在 Python 与 .NET 中运行 agents，允许它们彼此通信。分布式运行时使用 Microsoft Orleans 提供弹性、持久化，以及与 Azure Event Hubs 等消息服务的集成。xlang 功能要求 agent 的消息可序列化为 CloudEvents。消息通过 Grpc 以 CloudEvents 交换，运行时负责确保消息正确投递到对应 agent。

要使用分布式运行时，需要在项目中添加以下包：

```bash
dotnet add package Microsoft.AutoGen.Core.Grpc
```

该包运行在包含 agent 的应用中并连接到分布式系统。

运行后端/服务端需要：

```bash
dotnet add package Microsoft.AutoGen.RuntimeGateway
dotnet add package Microsoft.AutoGen.AgentHost
```

你可以单独运行后端：

```bash
dotnet run --project Microsoft.AutoGen.AgentHost
```

或将其集成到自己的应用中：

```csharp
using Microsoft.AutoGen.RuntimeGateway;
using Microsoft.AutoGen.AgentHost;
var autogenBackend = await Microsoft.AutoGen.RuntimeGateway.Grpc.Host.StartAsync(local: false, useGrpc: true).ConfigureAwait(false);
```

你也可以将运行时安装为 dotnet 工具：

```
dotnet pack --no-build --configuration Release --output './output/release' -bl\n
dotnet tool install --add-source ./output/release Microsoft.AutoGen.AgentHost
# 运行工具
# dotnet agenthost 
# 或者直接...
agenthost 
```

### 使用 .NET Aspire 在不同进程运行多个 Agent 与运行时

[Hello.AppHost 项目](https://github.com/microsoft/autogen/blob/50d7587a4649504af3bb79ab928b2a3882a1a394/dotnet/samples/Hello/Hello.AppHost/Program.cs#L4) 展示了如何使用 .NET Aspire 编排分布式系统，将多个 agent 与运行时运行在不同进程中。文中还引用了一个 [Python agent 示例](https://github.com/microsoft/autogen/blob/50d7587a4649504af3bb79ab928b2a3882a1a394/python/samples/core_xlang_hello_python_agent/README.md#L1)，用于展示如何在同一分布式系统中运行不同语言的 agents。

```csharp
// Copyright (c) Microsoft Corporation. All rights reserved.
// Program.cs

using Microsoft.Extensions.Hosting;

var builder = DistributedApplication.CreateBuilder(args);
var backend = builder.AddProject<Projects.Microsoft_AutoGen_AgentHost>("backend").WithExternalHttpEndpoints();
var client = builder.AddProject<Projects.HelloAgent>("HelloAgentsDotNET")
    .WithReference(backend)
    .WithEnvironment("AGENT_HOST", backend.GetEndpoint("https"))
    .WithEnvironment("STAY_ALIVE_ON_GOODBYE", "true")
    .WaitFor(backend);
// xlang 目前通过 http 通信 —— 生产环境应使用容器间 TLS
builder.AddPythonApp("HelloAgentsPython", "../../../../python/samples/core_xlang_hello_python_agent", "hello_python_agent.py", "../../.venv")
    .WithReference(backend)
    .WithEnvironment("AGENT_HOST", backend.GetEndpoint("http"))
    .WithEnvironment("STAY_ALIVE_ON_GOODBYE", "true")
    .WithEnvironment("GRPC_DNS_RESOLVER", "native")
    .WithOtlpExporter()
    .WaitFor(client);
using var app = builder.Build();
await app.StartAsync();
var url = backend.GetEndpoint("http").Url;
Console.WriteLine("Backend URL: " + url);
await app.WaitForShutdownAsync();
```

更多关于使用 Aspire 与 XLang agents 的示例见 [Microsoft.AutoGen.Integration.Tests.AppHost](https://github.com/microsoft/autogen/blob/acd7e864300e24a3ee67a89a916436e8894bb143/dotnet/test/Microsoft.AutoGen.Integration.Tests.AppHosts/) 目录。

### 配置日志

SDK 使用 Microsoft.Extensions.Logging 框架记录日志。以下 appsettings.json 示例包含一些有用的默认配置：

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "Microsoft.AspNetCore": "Information",
      "Microsoft": "Information",
      "Microsoft.Orleans": "Warning",
      "Orleans.Runtime": "Error",
      "Grpc": "Information"
    }
  },
  "AllowedHosts": "*",
  "Kestrel": {
    "EndpointDefaults": {
      "Protocols": "Http2"
    }
  }
}
```

### 在 Protocol Buffers 中定义消息类型

在 Python 与 .NET agents 中复用通用事件或消息类型的一种便捷方式是用 Protocol Buffers 定义事件。详见：[使用 Protocol Buffers 定义消息类型](./protobuf-message-types.md)。
