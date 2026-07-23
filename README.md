
# RELICS Commission Run Tracker

实时跟踪 RELICS 实验 Commission Run 各子系统进度的 Web 仪表盘。

## 项目概述

本项目用于管理 RELICS 实验 Commission Run 期间 **8 个子系统、80+ 项任务** 的进度跟踪、甘特图可视化和协作管理。支持基于 GitHub 的权限控制和 CODEOWNERS 自动审核机制。

**访问地址：** https://yangjijun1992.github.io/relics-commission-tracker/

**进度报告：** [progress_report.md](progress_report.md)

---

## 权限系统

### 登录流程

1. 访问页面 → 弹出登录框 → 输入全局密码
2. 登录后进入**只读模式**，可查看所有子系统数据
3. 点击「验证 GitHub 身份」→ 输入自己的 GitHub Personal Access Token (PAT)
4. 系统调用 GitHub API 验证用户身份 → 根据 `commission.json` 中的 `github_user` 字段判定权限

### 权限分级

| 角色 | 条件 | 权限 |
|------|------|------|
| 👑 管理员 | GitHub 用户 = `Yangjijun1992` | 编辑所有子系统、一键排序任务ID |
| 📝 子系统负责人 | GitHub 用户匹配子系统的 `github_user` | 仅编辑自己负责的子系统 |
| 👁️ 只读 | 未验证 GitHub 身份 | 只能查看，所有输入框禁用 |

### 全局访问凭证

| 字段 | 值 |
|------|-----|
| 用户名 | `relics10` |
| 密码 | `ComeOnRELICS!` |

### GitHub 用户名映射

| 子系统 | 负责人 | GitHub 用户名 |
|--------|--------|---------------|
| PDS | 杨继军 | `Yangjijun1992` |
| DAQ | 蔡畅 | `ChangCai-THU` |
| TPC | 谢凌峰 | `LingFeng-Xie` |
| Computing | 王俊 | `elphen-wang` |
| Cryo | 于佳成、李凯航 | `JiachenYu-123`, `Kaihang99` |
| Muon | 王俊、王笑宇 | `elphen-wang` |
| Shield | 岳玉用 | `Yueyuyong` |
| Facilities | 陈江宇 | `JiangyuChen853` |

---

## 功能特性

### 1. 进度追踪仪表盘

- **8 大子系统**：PDS、DAQ、TPC、Computing、Cryo、Muon、Shield、Facilities
- **Summary 统计栏**：总进度、任务总数、已完成/进行中/延迟统计、GitHub 用户映射状态
- **状态枚举**：`not_started` / `in_progress` / `completed` / `blocked` / `delayed`
- **进度可视化**：进度条 + 百分比数值，颜色按阈值自动变化

### 2. 甘特图时间线

- 点击子系统头部的 📊 按钮，在页面底部显示该子系统的甘特图
- 深色填充表示已完成进度比例
- 左侧显示任务中文名称
- "今天"标记线
- 管理员可一键按时间排序并重排任务 ID

### 3. 实时编辑（需 GitHub 身份验证）

- 网页端直接修改：任务名称、日期、负责人、状态、进度、备注
- 新增/删除子任务
- 子系统级别的负责人、时间范围可编辑
- 修改保存到浏览器 `localStorage`
- 导出/导入 JSON 文件

### 4. GitHub 集成推送

- 网页端配置 GitHub PAT
- 一键推送修改到仓库 `data/commission.json`

### 5. CODEOWNERS 自动生成

- 点击 **CODEOWNERS** 按钮生成文件
- 基于 `commission.json` 中 `github_user` 字段动态生成
- 支持项目管理员 + 子系统负责人分级审核

---

## 子系统总览

| 子系统 | ID | 中文名 | 负责人 | 时间范围 |
|--------|-----|--------|--------|----------|
| Photon Detection System | `pds` | 光子探测系统 | 杨继军 | 2026-06-22 ~ 2026-12-30 |
| DAQ System | `daq` | 数据采集系统 | 蔡畅 | 2026-07-01 ~ 2026-11-30 |
| TPC System | `tpc` | 时间投影室系统 | 谢凌峰 | 2026-04-28 ~ 2026-12-15 |
| Computing System | `computing` | 计算系统 | 王俊 | 2026-07-01 ~ 2026-11-15 |
| Cryogenics & Circulation | `cryo` | 低温与循环系统 | 于佳成、李凯航 | 2026-06-17 ~ 2026-12-30 |
| Muon Veto System | `muon` | 缪子反符合系统 | 王俊、王笑宇 | 2026-07-20 ~ 2026-11-30 |
| Shielding | `shield` | 屏蔽体系统 | 岳玉用 | 2026-07-10 ~ 2026-10-15 |
| Facilities | `fac` | 基础设施设备 | 陈江宇 | 2026-07-01 ~ 2026-12-01 |

---

## 技术架构

```
relics_commission/
├── index.html                    # 仪表盘主页（单文件SPA）
├── data/
│   └── commission.json           # 核心数据（JSON）
├── scripts/
│   ├── generate_codeowners.py    # CODEOWNERS 自动生成
│   ├── validate_commission.py    # 数据格式校验
│   └── generate_report.py        # 进度报告生成
├── progress_report.md            # 自动生成的进度报告
├── tpc_related/                  # TPC 参考资料（已 gitignore）
├── .github/
│   ├── CODEOWNERS                # 代码审核权限配置
│   └── workflows/
│       ├── deploy.yml            # GitHub Pages 自动部署
│       ├── generate-codeowners.yml # CODEOWNERS 自动生成
│       ├── validate-commission.yml # 数据校验
│       └── generate-report.yml   # 定时生成进度报告（每周一）
├── .gitignore
└── README.md
```

### 部署流程

```
Push to main → GitHub Actions (deploy.yml)
  → actions/checkout@v4
  → actions/configure-pages@v5
  → actions/upload-pages-artifact@v3
  → actions/deploy-pages@v4
  → GitHub Pages (yangjijun1992.github.io/relics-commission-tracker)
```

---

## 使用方式

### 本地预览

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

### 子系统负责人编辑流程

1. 打开 https://yangjijun1992.github.io/relics-commission-tracker/
2. 输入全局密码 `relics10` / `ComeOnRELICS!`
3. 点击「验证 GitHub 身份」，输入你的 GitHub PAT
4. 展开你负责的子系统，编辑任务字段
5. 修改保存在浏览器 `localStorage`
6. 点击 **Export JSON** 导出备份
7. 将导出的 JSON 通过 Pull Request 提交到仓库

### 管理员功能

- 编辑所有子系统
- 点击子系统头部的 📊 按钮查看该子系统甘特图
- 甘特图区域点击「按时间排序 ID」，自动按 `planned_start` 重新排列任务序号
- 修改 `github_user` 字段后点击 **CODEOWNERS** 按钮生成新配置

---

## 自动化工作流

| 工作流 | 触发条件 | 功能 |
|--------|----------|------|
| `deploy.yml` | Push to main | 自动部署到 GitHub Pages |
| `generate-codeowners.yml` | commission.json 变更 | 自动生成 CODEOWNERS |
| `validate-commission.yml` | PR / Push 涉及 commission.json | 校验数据格式 |
| `generate-report.yml` | 每周一 | 自动生成进度报告 |

### 常用命令

```bash
# 本地预览
python3 -m http.server 8000

# 数据校验
python3 scripts/validate_commission.py

# 生成 CODEOWNERS
python3 scripts/generate_codeowners.py

# 生成进度报告
python3 scripts/generate_report.py
```

---

## 相关文件说明

| 文件 | 用途 |
|------|------|
| `index.html` | 单文件 SPA 仪表盘，含登录/权限/甘特图 |
| `data/commission.json` | 核心进度数据 |
| `.github/CODEOWNERS` | 代码审核权限 |
| `.github/workflows/deploy.yml` | Pages 自动部署 |
| `.github/workflows/generate-codeowners.yml` | 自动生成 CODEOWNERS |
| `.github/workflows/validate-commission.yml` | PR 数据校验 |
| `.github/workflows/generate-report.yml` | 每周自动报告 |
| `scripts/generate_codeowners.py` | CODEOWNERS 生成脚本 |
| `scripts/validate_commission.py` | 数据校验脚本 |
| `scripts/generate_report.py` | 进度报告生成脚本 |
| `progress_report.md` | 自动生成的进度报告 |
| `.gitignore` | 忽略 tpc_related/、__pycache__/、.DS_Store |
