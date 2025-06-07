# 概述

## 基本概念

### CI/CD

CI/CD 是 **持续集成（Continuous Integration）** 和 **持续交付/部署（Continuous Delivery/Deployment）** 的缩写，是现代软件开发中用于自动化构建、测试和发布流程的一整套实践和工具。

### Gitea

Gitea 是一个轻量级的**自托管 Git 服务**，类似于 GitHub 或 GitLab。它提供了一个完整的 Git 平台，支持代码托管、协作开发、问题跟踪、拉取请求等功能。

### Gitea-Runner

Gitea-Runner 是 Gitea 的**自动化任务执行器**，用于实现 **CI/CD（持续集成/持续交付）** 功能。它与 GitHub Actions 的 Runner 类似，负责执行用户定义的工作流（Workflow）。

## 侧重

CI/CD 的实现有很多，相对于闭源的 Github，本篇实验报告侧重采用开源的 Gitea + Runner 来分析学习。

根据个人学习和使用 Gitea-CI/CD 的过程，并对部分感兴趣的细节深入探索研究，偏向于对于 CI/CD 与 GItea 实现的技术研究分析。

# Gitea 和 Runner 通信的方式[base.md](../../md2docx/test/testdata/base.md)

通过阅读源码和分析 docker 构建，其是基于 **HTTP/HTTPS 协议** 轮询发送请求。

比如状态的通知， 下图 `docker-compose.yml`中的 `RUNNER_CHECK_INTERVAL`参数，控制轮询的频率。

## **关键交互流程**

1. **任务获取**Runner 定期向 Gitea 的 `/api/actions/runner` 端点发送 `POST` 请求，查询是否有新任务（如 `push`、`pull_request` 等事件触发的工作流）。
2. **任务执行**当 Runner 获取到任务后，会从 Gitea 下载代码仓库、工作流配置和所需资源（通过 HTTP 拉取仓库归档或 Git 操作）。
3. **状态上报**
   Runner 在任务执行过程中，通过 HTTP API 实时向 Gitea 上报日志和状态（如"进行中"、"成功"、"失败"）。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749196506198-752cdd86-bf1c-4e50-8a2c-c22eb0b256e0.png)

# Job 中访问 actions 预动作仓库采取的协议

默认情况下需要对应的仓库会以 https 的方式拉取 github 上的 actions 仓库。

而在 Gitea/GitHub Actions的工作流配置中，默认使用HTTPS协议拉取预定义动作仓库的原因主要涉及以下几个方面：

1. **HTTPS的优势**：
   - **无需额外配置**：HTTPS协议无需配置RSA密钥对，普通用户可以直接通过HTTPS URL访问公共仓库，简化了配置流程。
   - **广泛的网络支持**：HTTPS作为标准的网络协议，可以在大多数网络环境下正常工作，不需要复杂的网络配置。
   - **匿名访问能力**：对于公开的Actions仓库，可以通过HTTPS直接进行拉取，无需身份认证。
2. **SSH协议的限制**：
   - **密钥管理复杂**：使用SSH协议需要配置SSH私钥，并确保私钥的安全性。在CI/CD环境中管理SSH密钥会增加配置复杂度。
   - **权限控制要求高**：SSH需要严格的权限控制，稍有不慎可能导致安全问题。在自动化任务中管理SSH密钥可能带来更高的安全风险。
   - **配置步骤繁琐**：需要在Gitea Actions的工作流中注入SSH密钥，并进行相应的权限配置，这对普通用户提出了更高的技术要求。
3. **Gitea/GitHub Actions的环境限制**：在GitHub的托管环境中，配置SSH密钥需要通过特定的方式进行注入，这与传统的开发环境有所不同。虽然**Gitea** Actions支持SSH协议，但需要额外的步骤来配置密钥，而默认情况下使用HTTPS可以提供更便捷的使用体验。
4. **使用场景分析**：当需要访问私有仓库或对安全性有更高要求时，SSH协议仍然是更好的选择。但此时需要通过Gitea Actions的 Secrets功能妥善管理SSH密钥，并配置相应的权限。
   综上所述，HTTPS作为默认的拉取方式，在提供便利性的同时，也很好地平衡了安全性和易用性的关系。在需要更高安全性的场景下，用户仍然可以选择SSH协议，但需要做好相应的配置和安全管理。

# Runner-Actions 与安全

## Runner 的部署与 token 认证

类似一般的 jwt 风格的 token 认证方式，runner 在向主机的 gitea 发送 HTTP 请求的时候会依靠 token 作为鉴权认证，确保一定的安全性。

不过和一般 jwt 不同的是，这类 token 并不适合频繁的切换，所以安全性上或许也略差一些。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749196569700-55405df2-1e10-4d46-bbc4-36fbcbb4c228.png)

## actions 中的"变量/密钥"概念

将账号密码等隐私信息保存到 gitea 用户中，而非暴露在 actions 的编写中，具有更好的安全性。

在 act_runner 的源码中，也是通过从 Gitea 拿到对应的 secrets 和 vars，然后处理 actions 中的占位符。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749261624374-c62b84cd-24d4-43c3-8fbf-4d8d7b757edb.png)

# Runner 如何控制 docker

[act_runner](https://gitea.com/gitea/act_runner)

## 核心通信实现

act_runner 主要通过 `github.com/docker/docker/client` 包与 Docker 进行通信。

在 `internal/pkg/envcheck/docker.go` 中可以看到基本的 Docker 客户端初始化和连接检查逻辑。

## 主要通信场景

在 `internal/app/run/runner.go` 中，runner 会通过 Docker 客户端来：

1. 创建和管理容器
2. 设置容器配置（如网络模式、挂载卷等）
3. 执行工作流任务

## 部署模式

项目支持多种 Docker 部署模式。

1. 基本模式：直接使用主机的 Docker daemon；
2. Docker-in-Docker (DinD)：在容器内运行 Docker；比如我在实验中就是采用 docker 的方式部署 act_runner，那么就会出现 DinD 这样的现象。
3. Rootless Docker：使用非 root 用户运行 Docker。

# Runner 如何使得 uses 生效

在一个 Actions 中我们或多或少会用到第三方写好的 actions，而这些 actions 各式各样。从宏观上观察 runner 在拉取到目标仓库之后传入自定义参数执行对应的操作。

这一部分我们可以参看 nektos/act 的官方介绍：

> When you run act it reads in your GitHub Actions from .github/workflows/ and determines the set of actions that need to be run. It uses the Docker API to either pull or build the necessary images, as defined in your workflow files and finally determines the execution path based on the dependencies that were defined. Once it has the execution path, it then uses the Docker API to run containers for each action based on the images prepared earlier. The environment variables and filesystem are all configured to match what GitHub provides.

[GitHub - nektos/act: Run your GitHub Actions locally 🚀](https://github.com/nektos/act)

而也如 gitea 的 act_runner 所言，act_runner 可以看作是 act 的一个适配器。

> nektos/act 项目是一个优秀的工具，允许你在本地运行GitHub Actions。 我们受到了它的启发，并思考它是否可能为Gitea运行Actions。
>
> 然而，尽管nektos/act被设计为一个命令行工具，但我们实际上需要的是一个专为Gitea修改的Go库。 因此，我们在gitea/act基础上进行了分叉。

[Gitea Actions设计 | Gitea Documentation](https://docs.gitea.com/zh-cn/usage/actions/design)

那么继续分析一些 act 的源码。（ps. 题外话，这样的 step - job 的架构设计，和最近较为热门的 Agent 技术异曲同工，都是在以"任务分步骤做"这样的类似 CoT 的概念来设计）

## Action 解析流程

当遇到 uses 字段时，act 首先会解析 action 的引用格式，通常是 `{org}/{repo}[/path]@ref `的形式，以及这里默认 `base_url` 为 github，但在 act_runner 中也将此处理为自定义字段，方便了一些无法稳定访问 github 的国内服务器处理。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749265622157-77846167-9c2c-4111-af3e-9ad326619fcf.png)

另外，act 对于 actions/checkout 这样的常用动作，采用了从本地获取优化的处理方案。其他的借助 git 从第三方仓库克隆。![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749265879440-07876439-80a0-4c43-92ae-26e473771f28.png)

## Action 类型支持与执行机制

这一部分实际是 actions 提供者设计诸如 `action.yml`这样的配置文件来"指导"`act` 执行具体的任务。

比如常见的有以下几种，其中基于 docker 在环境上更加灵活，不过也有很多的 actions 是采用 ts 编写的，故 `Node.js` 的使用也不在少数，

1. Node.js Actions

将 action 代码复制到容器中

使用 Node.js 运行时执行 action 的入口文件

支持通过 trampoline.js 处理命令行参数

2. Docker Actions

支持使用 Dockerfile 或预构建的 Docker 镜像

在容器中执行 action

支持环境变量和参数传递

3. Composite Actions

支持组合多个步骤

可以包含多个命令和脚本

支持跨平台执行![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749266150572-2a606459-b5c9-4e62-ac7b-a37da9e8aa0f.png)

## 优点

1. 灵活性：支持多种类型的 action 和编程语言
2. 隔离性：通过容器确保执行环境的安全和隔离
3. 可扩展性：可以轻松添加新的 action 类型支持
4. 兼容性：与 GitHub Actions 保持高度兼容

## 案例分析：actions/checkout 的 actions.yml

### 介绍

`actions/checkout` 是 GitHub 官方提供的 Action，用于在 CI/CD 工作流中检出代码到 Runner。

[GitHub - actions/checkout: Action for checking out a repo](https://github.com/actions/checkout)

### 分析

使用 runs 标签指定环境和入口。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749266828066-422559fc-da33-4133-8fd0-45d005ccb086.png)

基本 IO，输入输出参数的设定。

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749267014872-b5a34f81-9078-4088-954c-31e0286b2c1f.png)

# Runner 中控制目标服务器执行任务的方式

在 CI/CD 流程中，Runner 访问目标服务器进行操作的方式主要有两种：SSH 连接 和 Webhook 触发。以下是两种方式的详细介绍及其优缺点。

## ssh 连接到目标服务器操作

### 实现方式

Runner 通过 SSH（Secure Shell）协议连接到目标服务器，执行预定义的命令或脚本。通常需要在 Runner 和目标服务器之间配置 SSH 密钥对，以实现免密码登录。

### 优点

安全性高：SSH 协议采用加密通信，确保数据传输的安全性。

灵活性强：可以直接执行任意命令或脚本，适合复杂的操作需求。

环境隔离：通过 SSH 连接到目标服务器，可以确保操作环境与 Runner 环境隔离，避免相互影响。

### 缺点

配置复杂：需要生成和分发 SSH 密钥，并确保 Runner 能够访问目标服务器。

保持长连接：SSH 连接需要保持长连接状态，以确保 Runner 能够持续与目标服务器通信。如果网络不稳定或中断，SSH 连接可能会断开，导致正在执行的任务失败，需要额外的机制（如自动重连）来保证任务连续性。

### 案例

![](https://cdn.nlark.com/yuque/0/2025/png/52164547/1749260642508-1d5c8b7a-973c-4de2-9e47-e97a8602ceb4.png)

## 通过 webhooks 触发

### 实现方式：

Runner 通过 HTTP/HTTPS 请求向目标服务器发送 Webhook，触发目标服务器上的操作。目标服务器需要实现 Webhook 接收接口，并根据 Webhook 的内容执行相应的操作。

### 优点

简单易用：只需在目标服务器上配置 Webhook 接收接口，无需复杂的 SSH 配置。

解耦性强：Runner 和目标服务器之间通过 Webhook 通信，降低了系统间的耦合性。

跨网络支持：Webhook 可以通过公网访问，适合分布式环境。

### 缺点

安全性依赖配置：需要确保 Webhook 的认证机制（如 Token 验证）足够安全，防止未授权访问。

操作受限：只能触发目标服务器上预定义的操作，灵活性不如 SSH。

网络延迟：Webhook 请求的响应时间可能影响整体流程的执行速度。

# 结语

通过对 Gitea + Runner 的 CI/CD 实现分析，我们可以看到现代软件开发中自动化流程的重要性。本文从技术实现的角度，深入探讨了以下几个关键方面：

1. **通信机制**：Runner 与 Gitea 之间基于 HTTP/HTTPS 的轮询通信方式，展示了分布式系统中常见的通信模式。
2. **安全性考虑**：从 token 认证到 secrets 管理，体现了 CI/CD 系统中安全性的重要性。
3. **容器化支持**：通过 Docker 实现任务隔离和执行环境管理，展示了容器技术在 CI/CD 中的核心作用。
4. **扩展性设计**：支持多种类型的 actions 和灵活的部署模式，体现了系统的可扩展性。

这些技术实现不仅适用于 Gitea，也为其他 CI/CD 系统的设计和实现提供了参考。随着云原生和 DevOps 的发展，CI/CD 将继续在软件开发中扮演重要角色，而开源实现如 Gitea + Runner 则为开发者提供了更多选择和学习的空间。

未来，随着技术的演进，我们可能会看到更多创新的 CI/CD 实现方式，但核心目标始终是提高开发效率、保证代码质量和加速软件交付的云计算时代。
