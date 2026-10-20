# 贡献指南 | Contributing Guide

**SINOSHOP-OS 海洋空间智能生态母体 — 开放协作框架**

---

## 💻 环境准备

**安装 Python（推荐 3.10+）**
- Windows: 从 [python.org](https://www.python.org/downloads/) 下载安装包
- macOS: rew install python@3.10
- Linux: sudo apt install python3.10 python3.10-venv

**验证安装**
 + ```bash
python --version
pip --version
 + ```

如果  `pip`  命令不可用，请使用  `python -m pip`  代替。

---

## 🚀 5 分钟快速开始

**第一步：选一个任务**
从 [Good First Issues](https://gitee.com/sinoshop/sinoshop-os/issues?label=Good%20First%20Issue) 中挑一个你感兴趣的。

**第二步：克隆仓库**
 + ```bash
git clone https://gitee.com/sinoshop/sinoshop-os.git
cd sinoshop-os
 + ```

**第三步：创建分支**
 + ```bash
git checkout -b your-name/issue-number
 + ```

**第四步：写代码 & 签名提交**
 + ```bash
git add .
git commit -s -m "fix: 描述你的修改"
git push origin your-name/issue-number
 + ```

**第五步：提交 PR**
打开 Gitee 仓库页面，点击「Pull Requests」→「新建 Pull Request」。

> ⚠️ 所有提交必须使用  `git commit -s`  进行 DCO 签名，否则 CI 会拦截。

---

## DCO 签名要求

所有提交必须包含 **Signed-off-by** 签名，以此确认：

- ✅ 你有权提交此代码
- ✅ 代码符合 Apache 2.0 许可
- ✅ 你已阅读并同意 [CLA.md](./CLA.md)

**操作方式：**
 + ```bash
git commit -s -m "feat: 你的提交说明"
 + ```

> 无签名的 Pull Request 将在 CI 阶段被自动标记，需补充签名后方可合并。

---

## 分级贡献者路径

| 等级 | 角色 | 权限 | 晋升条件 |
|---|---|---|---|
| **L1 — Explorer** | 首次贡献者 | 提交 Issue，参与讨论 | 提交并被合并 1 个 PR |
| **L2 — Architect** | 子系统优化者 | 提交代码，参与设计评审 | 已合并 5+ 个实质性 PR |
| **L3 — Maintainer** | 核心维护者 | 代码合并权，进入 TSC | TSC 委员会投票通过 |

---

## 联系方式

- **技术讨论**：Gitee Issues / GitHub Issues
- **邮箱**：standards@sinoshop.org

---

**SINOSHOP-Core 技术团队**
苏月明、梁诚超、梁振雄
