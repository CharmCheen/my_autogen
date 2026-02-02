# Agent 与 Topic ID 规范

本文档描述 Agent ID 与 Topic ID 的结构、约束与行为。

## Agent ID

### 必填属性

#### type

- 类型：`string`
- 说明：agent type 不是 agent 类本身。它将 agent 与特定工厂函数关联，该工厂函数用于生成同一 agent `type` 的实例。例如，不同的工厂函数可以生成相同的 agent 类，但使用不同的构造参数。
- 约束：UTF8，仅包含字母（a-z）、数字（0-9）或下划线（_）。有效标识符不能以数字开头，且不能包含空格。
- 示例：
  - `code_reviewer`
  - `WebSurfer`
  - `UserProxy`

#### key

- 类型：`string`
- 说明：agent key 是给定 agent `type` 的实例标识符
- 约束：UTF8，仅包含 ASCII 32（空格）到 126（~）之间的字符（含边界）。
- 示例：
  - `default`
  - 某个内存地址
  - UUID 字符串

## Topic ID

### 必填属性

#### type

- 类型：`string`
- 说明：topic type 通常由应用代码定义，用于标识该主题承载的消息类型。
- 约束：UTF8，仅包含字母（a-z）、数字（0-9）、`:`、`=` 或下划线（_）。有效标识符不能以数字开头，且不能包含空格。
- 示例：
  - `GitHub_Issues`

#### source

- 类型：`string`
- 说明：topic source 是某个 topic type 下的唯一主题标识，通常由应用数据定义。
- 约束：UTF8，仅包含 ASCII 32（空格）到 126（~）之间的字符（含边界）。
- 示例：
  - `github.com/{repo_name}/issues/{issue_number}`
