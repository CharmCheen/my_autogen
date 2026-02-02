# Agent Worker 协议

## 系统架构

系统由多个进程组成，每个进程要么是 _service_ 进程，要么是 _worker_ 进程。
worker 进程承载应用代码（agents）并连接到 service 进程。
worker 会向 service 声明其支持的 agent，使得 service 可以决定将 agent 放置到哪个 worker 上。
service 进程负责协调 agents 在 worker 进程上的放置，并促进 agents 之间的通信。

agent 实例由 `(namespace: str, name: str)` 这一元组标识。
`namespace` 与 `name` 均由应用定义。
`namespace` 在系统层面没有预设语义：它是自由格式，具体语义由应用代码实现。
`name` 用于将请求路由到支持该名称的 worker。
worker 会向 service 声明其能够承载的 agent 名称集合。
worker 在收到来自 service 的消息后激活 agent。
service 使用 `name` 决定将当前不活跃的 agent 放置到哪个 worker 上，并维护从 agent 名称到支持该 agent 的 worker 集合的映射。
service 维护一个 _directory_，将活跃的 agent id 映射到承载该 agent 的 worker 进程。

### Agent 生命周期

agent 不会被显式创建或销毁。当收到对当前不活跃 agent 的请求时，service 负责选择能够承载该 agent 的 worker，并将请求路由到该 worker。

## Worker 协议流程

worker 协议有三个阶段，贯穿 worker 的生命周期：初始化、运行、终止。

### 初始化

worker 进程启动时，会与 service 进程建立连接，形成双向通信通道，用于消息传递。
随后，worker 会发送零个或多个 `RegisterAgentType(name: str)` 消息，告知 service 自己能够承载的 agent 名称。

* TODO：worker 还应向 service 提供哪些元数据？
* TODO：是否应为 worker 分配可在其生命周期内识别的唯一 id？是否允许由 worker 进程自行指定？

### 运行

连接建立且 service 知道 worker 可承载哪些 agent 之后，worker 开始接收需要其承载的 agent 请求。
agent 的放置由 `Event(...)` 或 `RpcRequest(...)` 消息触发。
worker 维护一个本地活跃 agent 的 _catalog_：从 agent id 到 agent 实例的映射。
如果收到某个 agent 的消息但 catalog 中没有对应条目，worker 会激活该 agent 的新实例并插入到 catalog。
worker 将消息分派给 agent：

* 对于 `Event`，agent 处理消息但不生成响应。
* 对于 `RpcRequest`，agent 处理消息并生成 `RpcResponse` 响应。worker 将响应路由回原始发送者。

worker 维护一个待处理请求映射（由 `RpcRequest.id` 标识），对应一个未来的 `RpcResponse`。收到 `RpcResponse` 后，worker 找到对应请求 id 并用该响应兑现 promise。
若在指定时间内（例如 30 秒）未收到响应，worker 将以超时错误终止该 promise。

### 终止

当 worker 准备关闭时，会关闭与 service 的连接并终止。service 将注销该 worker 以及其承载的所有 agent 实例。
