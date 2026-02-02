# 编程模型

理解你的工作流并将其映射到 agent，是在 AutoGen 中构建 agent 系统的关键。

编程模型本质上是发布-订阅。agent 订阅自己关心的事件，也可以发布其他 agent 可能关心的事件。agent 还可以拥有额外资产，如 Memory、提示词、数据源与技能（外部 API）。

## 以 CloudEvents 交付事件

系统中的每个事件都使用 [CloudEvents 规范](https://cloudevents.io/) 定义。这使得事件格式在不同系统与语言之间保持一致。在 CloudEvents 中，每个事件都有必须包含的“上下文属性”：

1. *id* - 唯一标识（例如 UUID）。
2. *source* - 指示事件来源的 URI 或 URN。
3. *type* - 事件命名空间，使用反向 DNS 前缀。
   - 前缀域名决定定义该事件类型语义的组织，例如 `com.github.pull_request.opened` 或 `com.example.object.deleted.v2`，并可选包含描述数据 schema/内容类型或扩展的字段。

## 事件处理器

每个 agent 都有一组事件处理器，绑定到某个 CloudEvents *type* 的匹配条件。事件处理器可以匹配精确类型，也可以匹配类型层级中的某一层级模式（例如 `com.Microsoft.AutoGen.Agents.System.*` 用于匹配 `System` 命名空间中的所有事件）。每个事件处理器都是一个函数，可用于改变状态、调用模型、访问记忆、调用外部工具、发出其他事件，以及与其他系统进行数据流转。事件处理器既可以是简单函数，也可以是使用状态机或其他控制逻辑的复杂函数。

## 编排 agents

你可以构建一个只对外部事件做出反应的可用且可扩展的 agent 系统。但在很多情况下，你会希望编排 agents 以实现特定目标或遵循预设流程。这时需要构建一个编排器 agent，用于管理 agents 之间的事件流转。

## 内置事件类型

AutoGen 系统提供了一组用于系统管理的内置事件类型，包括：

- *System Events* - 用于管理系统本身的事件，例如启动/停止 agents、向所有 agents 发送消息等系统级事件。
- *在此插入其他类型*

## Agent 合约

你可能希望使用更具规范性的 agent 行为合约。AutoGen 也提供了基础 agent，实现不同的行为方式，包括在事件驱动模型之上叠加请求/响应模式。示例可参考 Python 示例中的 ChatAgents。此时你的 agent 需要实现一组已知事件，并遵循这些事件预期的特定行为。
