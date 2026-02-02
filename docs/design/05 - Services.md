# AutoGen 服务

## 概述

每个 AutoGen agent 系统都包含一个或多个 Agent Worker 以及一组用于管理/支持 agents 的服务。服务与 worker 可以部署在同一进程中，也可以分布式部署。在同一进程中，通信与事件投递在内存中进行；分布式情况下，worker 通过 gRPC 与服务通信。无论哪种情况，事件都以 CloudEvents 封装。后端服务有多种选项：

- 内存模式：Agent Worker 与 Services 部署在同一进程内，通过内存通道通信。Python 与 .NET 均可用。
- 仅 Python：Agent Worker 与一个由 Python 承载的服务通信，该服务实现内存消息总线与 agent 注册表。
- Microsoft Orleans：分布式 actor 系统，可承载服务与 worker，提供带持久化存储的分布式状态，支持多种事件总线类型，并支持跨语言 agent 通信。
- *路线图：支持其他语言的分布式系统，如 dapr 或 Akka。*

系统中的服务包括：

- Worker：承载 agents，并作为 Gateway 的客户端
- Gateway：
-- 其他服务 API 的 RPC 网关
-- 在 worker 与 Event Bus 之间提供 RPC 桥接
-- 消息会话状态（跟踪消息队列/投递）
- Registry：跟踪系统中的 {agents:agent types}:{Subscription/Topics} 以及它们可处理的事件
-- *路线图：在 Gateway 中添加查询 API*
- AgentState：agent 的持久化状态
- Routing：根据订阅+主题将事件投递给 agent
-- *路线图：添加订阅管理 API*
- *路线图：Agent 系统管理 API*
- *路线图：调度：管理 agent 的放置*
- *路线图：发现：支持发现 agents 与服务*
