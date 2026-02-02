---
_disableAffix: true
---

<div class="center">
    <h1>AutoGen .NET</h1>
    <p class="subheader">
    用于构建 AI 智能体与应用的 <i>.NET</i> 框架
    </p>
</div>

<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Core</h5>
<p>

[![dotnet-ci](https://github.com/microsoft/autogen/actions/workflows/dotnet-build.yml/badge.svg)](https://github.com/microsoft/autogen/actions/workflows/dotnet-build.yml)
[![NuGet version](https://badge.fury.io/nu/Microsoft.AutoGen.Contracts.svg)](https://badge.fury.io/nu/Microsoft.AutoGen.Contracts)
[![NuGet version](https://badge.fury.io/nu/Microsoft.AutoGen.Core.svg)](https://badge.fury.io/nu/Microsoft.AutoGen.Core)
[![NuGet version](https://badge.fury.io/nu/Microsoft.AutoGen.Core.Grpc.svg)](https://badge.fury.io/nu/Microsoft.AutoGen.Core.Grpc)
[![NuGet version](https://badge.fury.io/nu/Microsoft.AutoGen.RuntimeGateway.Grpc.svg)](https://badge.fury.io/nu/Microsoft.AutoGen.RuntimeGateway.Grpc)
[![NuGet version](https://badge.fury.io/nu/Microsoft.AutoGen.AgentHost.svg)](https://badge.fury.io/nu/Microsoft.AutoGen.AgentHost)

</p>
        <p class="card-text">用于构建可扩展多智能体 AI 系统的事件驱动编程框架。</p>

- 面向业务流程的确定性与动态智能体工作流
- 多智能体协作研究
- 面向多语言应用的分布式智能体
- 与事件驱动、云原生应用集成

*如果你要构建工作流或分布式智能体系统，请从这里开始*

<p>
<div class="highlight">
<pre id="codecell0" tabindex="0">

```bash
dotnet add package Microsoft.AutoGen.Contracts
dotnet add package Microsoft.AutoGen.Core

# 可选：用于分布式智能体系统

dotnet add package Microsoft.AutoGen.RuntimeGateway.Grpc
dotnet add package Microsoft.AutoGen.AgentHost

# 其他可选包

dotnet add package Microsoft.AutoGen.Agents
dotnet add package Microsoft.AutoGen.Extensions.Aspire
dotnet add package Microsoft.AutoGen.Extensions.MEAI
dotnet add package Microsoft.AutoGen.Extensions.SemanticKernel
```

</pre></div></p>
<p>
        <a href="core/index.md" class="btn btn-primary">开始使用</a>
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">AgentChat</h5>
        <p class="card-text">用于构建对话式单智能体与多智能体应用的编程框架，构建于 Core 之上。</p>
        <a href="#" class="btn btn-primary disabled">即将推出</a>
      </div>
    </div>
  </div>
</div>
