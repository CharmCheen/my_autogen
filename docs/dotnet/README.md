# 如何构建并运行网站

## 前置条件

- dotnet 8.0 或更高版本

## 构建

首先进入 autogen/dotnet 目录，并运行以下命令构建网站：

```bash
dotnet tool restore
dotnet tool run docfx ../docs/dotnet/docfx.json --serve
```

命令执行完成后，打开浏览器访问 `http://localhost:8080` 即可查看网站。
