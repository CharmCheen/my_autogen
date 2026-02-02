# 主题（Topics）

本文档描述发布消息与订阅主题的语义与组成部分。

## 概述

主题用于管理哪些 agent 接收某条已发布消息。agent 订阅主题。应用定义从主题到 agent 实例的映射。

这些概念有意与 [CloudEvents](https://cloudevents.io/) 规范对齐，便于与现有系统和工具集成。

### 非目标

本文档不定义 RPC/直接消息。

## 标识符

一个主题由两个组件标识（称为 `TopicId`）：

- [`type`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type) - 表示事件发生的类型，静态且在代码中定义
  - 应使用反向域名表示法以避免命名冲突，例如：`com.example.my-topic`。
  - 允许值必须匹配正则：`^[\w\-\.\:\=]+\Z`
  - 需要注意：这与 agent type 相同，但允许额外的 `=` 与 `:` 字符
- [`source`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1) - 表示事件来源，动态且基于消息本身
  - 应为 URI

agent 实例由两个组件标识（称为 `AgentId`）：

- `type` - 表示 agent 类型，静态且在代码中定义
  - 允许值必须匹配正则：`^[\w\-\.]+\Z`
- `key` - 表示某个 agent 类型的具体实例
  - 应为 URI

例如：`GraphicDesigner:1234`

## 订阅

订阅定义哪些 agent 接收发布到某个主题的消息。订阅是动态的，可随时添加或移除。

一个订阅定义两件事：

- 匹配函数 `TopicId -> bool`，用于判断“该订阅是否匹配该主题”
- 映射函数 `TopicId -> AgentId`，用于判断“匹配后映射到哪个 agent”

这些函数必须无副作用，以便评估结果可以缓存。

### Agent 实例创建

如果主题映射到的 agent 尚不存在，运行时会实例化该 agent 以完成请求。

## 消息类型

agent 可以处理某些类型的消息，这是 agent 实现的内部细节。通道内所有 agent 都会收到所有消息，但会忽略不能处理的消息。

> [!NOTE]
> 可能会基于规模与性能考虑在未来调整此行为。

## 约定主题类型

agent 应通过前缀订阅 `{AgentType}:` 主题，将其作为该 agent 类型的直达消息通道。

此订阅的 source 应直接映射到 agent key。

因此该订阅将接收以下约定主题的所有事件：

- `{AgentType}:` - 通用直达消息，应路由到对应消息处理器。
- `{AgentType}:rpc_request={RequesterAgentType}` - RPC 请求消息，应路由到对应 RPC 处理器，且使用 RequesterAgentType 发布响应。
- `{AgentType}:rpc_response={RequestId}` - RPC 响应消息，应路由回调用方响应 future。
- `{AgentType}:error={RequestId}` - 与给定请求对应的错误消息。
