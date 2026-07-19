# RELICS Commission Run Tracker

实时跟踪 RELICS 实验 Commission Run 各子系统进度的 Web 仪表盘。

## 项目概述

本项目用于管理 RELICS 实验 Commission Run 期间 **8 个子系统、80+ 项任务** 的进度跟踪、甘特图可视化和协作管理。支持自定义域名访问、基于 GitHub 的权限控制和 CODEOWNERS 自动审核机制。

**访问地址：** `https://relics.tracker.com`（需完成 DNS 配置后生效）

---

## 功能特性

### 1. 进度追踪仪表盘

- **8 大子系统**：PDS、DAQ、TPC、Computing、Cryo、Muon、Shield、Facilities
- **80 项子任务**：含任务ID、中英文名称、起止日期、负责人、状态、进度百分比、备注
- **Summary 统计栏**：总进度、任务总数、已完成/进行中/阻塞/延迟统计、子系统数量、GitHub 用户映射状态
- **状态枚举**：`not_started` / `in_progress` / `completed` / `blocked` / `delayed`
- **进度可视化**：进度条 + 百分比数值，颜色按阈值自动变化

### 2. 甘特图时间线

- 自动计算全局时间范围（2026-04-28 ~ 2026-12-30）
- 按子系统分色显示任务条
- 深色填充表示已完成进度比例
- 鼠标悬停显示详细信息

### 3. 实时编辑

- 网页端直接修改：任务名称、日期、负责人、状态、进度、备注
- 子系统级别的负责人、时间范围可编辑
- **新增/删除子任务**：每个子系统可动态增删
- 修改自动保存到浏览器 `localStorage`
- 导出/导入 JSON 文件（手动持久化）

### 4. GitHub 集成推送

- 网页端配置 GitHub Personal Access Token (PAT)
- 一键推送修改到仓库 `data/commission.json`
- 自动获取文件 SHA 并创建 commit

### 5. 负责人 → GitHub 用户名映射

- 每个子系统头部显示负责人姓名 + GitHub 用户名徽章
- 紫色徽章 = 已分配，黄色徽章 = 待填写（TBD）
- GitHub 用户名可内联编辑
- Summary 栏统计已分配/待填写数量

### 6. CODEOWNERS 自动生成

- 点击 **CODEOWNERS** 按钮，根据当前映射自动生成 `.github/CODEOWNERS` 文件
- 基于 `commission.json` 中的 `github_user` 字段动态生成
- 支持项目级管理员 + 子系统负责人分级审核

---

## 子系统总览

| 子系统 | ID | 中文名 | 负责人 | 任务数 | 时间范围 |
|--------|-----|--------|--------|--------|----------|
| Photon Detection System | `pds` | 光子探测系统 | 杨继军 | 13 | 06-22 ~ 12-30 |
| DAQ System | `daq` | 数据采集系统 | 蔡畅、雷阳、杨继军 | 9 | 07-01 ~ 11-30 |
| TPC System | `tpc` | 时间投影室系统 | 谢凌峰 | 18 | 04-28 ~ 12-15 |
| Computing System | `computing` | 计算系统 | 王俊 | 8 | 07-01 ~ 11-15 |
| Cryogenics & Circulation | `cryo` | 低温与循环系统 | 于佳成 | 12 | 06-17 ~ 12-30 |
| Muon Veto System | `muon` | 缪子反符合系统 | 王俊、王笑宇 | 7 | 07-20 ~ 11-30 |
| Shielding | `shield` | 屏蔽体系统 | 岳玉用 | 5 | 07-10 ~ 10-15 |
| Facilities | `fac` | 基础设施设备 | 陈江宇 | 8 | 07-01 ~ 12-01 |

---

## 数据来源与合并历史

### TPC 子系统数据合并（2026-07-19）

将 Jupyter Notebook 中的 **29 项 TPC 细粒度任务** 与 commission.json 现有任务进行了全面对比分析后合并：

**合并结果：**

| 子系统 | 原任务数 | 新增 | 现任务数 |
|--------|----------|------|----------|
| PDS | 10 | +3 | 13 |
| TPC | 8 | +10 | 18 |
| Cryo | 8 | +4 | 12 |
| **合计** | 64 | **+17** | **80** |

**新增任务类别：**
- TPC：场笼零件加工、电极测试、液位计、电容传感器、馈通采购测试、安装支架、cryostat连接、罐内走线、水平调整、移动馈通
- PDS：PMT选型排列、读出电路线缆、标定扩散棒加工
- Cryo：低温恒温罐设计、溢流腔设计、进液接头定制、进液管制作

**修复：** PDS 重复 `pds-08` ID → 改为 `pds-10`

---

## 权限管理

### 角色层级

```
项目管理者 (Yangjijun1992)
├── 所有文件的最终审核权
├── main 分支保护（require PR + review）
├── CODEOWNERS 管理
└── 部署配置管理

子系统负责人 (各子系统 github_user)
├── 对应子系统任务的审核权
├── PR review 权限
└── 通过 Fork + PR 提交修改

协作成员
├── Fork 仓库
├── 修改后提 PR
└── 等待审核合并
```

### 工作流程

```
1. 协作者 Fork 仓库
2. 本地修改 data/commission.json
3. Push 到自己的 Fork
4. 向 main 分支提 Pull Request
5. CODEOWNERS 自动通知对应子系统负责人
6. 至少 1 人 Approved 后合并
7. GitHub Actions 自动部署到 Pages
```

### GitHub 用户名映射

在 `data/commission.json` 的每个子系统中，`github_user` 字段用于：

- CODEOWNERS 自动生成
- PR review 自动分配
- 网页端显示和编辑

| 子系统 | 负责人 | GitHub 用户名 |
|--------|--------|---------------|
| PDS | 杨继军 | `Yangjijun1992` ✅ |
| DAQ | 蔡畅、雷阳、杨继军 | `Yangjijun1992` ✅ |
| TPC | 谢凌峰 | ⏳ 待填写 |
| Computing | 王俊 | ⏳ 待填写 |
| Cryo | 于佳成 | ⏳ 待填写 |
| Muon | 王俊、王笑宇 | ⏳ 待填写 |
| Shield | 岳玉用 | ⏳ 待填写 |
| Facilities | 陈江宇 | ⏳ 待填写 |

---

## 技术架构

```
relics_commission/
├── index.html                    # 仪表盘主页（单文件SPA）
├── CNAME                         # 自定义域名配置 → relics.tracker.com
├── data/
│   └── commission.json           # 核心数据（JSON）
├── tpc_related/                  # TPC 参考资料（已 gitignore）
│   └── jupyter-notebook/         # Jupyter Notebook + 甘特图输出
├── .github/
│   ├── CODEOWNERS                # 代码审核权限配置
│   └── workflows/
│       └── deploy.yml            # GitHub Pages 自动部署
├── .gitignore                    # 忽略 tpc_related/、__pycache__/ 等
└── README.md
```

### JSON 数据结构

```json
{
  "project": {
    "name": "RELICS Experiment Commission Run",
    "description": "RELICS实验Commission Run进度跟踪",
    "pi": "PI Name",
    "start_date": "2026-04-28",
    "end_date": "2026-12-31"
  },
  "subsystems": [
    {
      "id": "tpc",
      "name": "TPC System",
      "name_cn": "时间投影室系统",
      "responsible": "谢凌峰",
      "github_user": "TBD-xielingfeng",
      "planned_start": "2026-04-28",
      "planned_end": "2026-12-15",
      "subtasks": [
        {
          "id": "tpc-pre-01",
          "name": "Field Cage Parts Manufacturing",
          "name_cn": "场笼零件加工",
          "planned_start": "2026-04-28",
          "planned_end": "2026-07-21",
          "status": "in_progress",
          "progress": 55,
          "assignee": "谢凌峰",
          "notes": "含PEEK压板、PTFE反射壁、整形环等"
        }
      ]
    }
  ],
  "last_updated": "2026-07-19T17:30:00"
}
```

### 部署流程

```
Push to main → GitHub Actions (deploy.yml)
  → actions/checkout@v4
  → actions/configure-pages@v5
  → actions/upload-pages-artifact@v3 (path: '.')
  → actions/deploy-pages@v4
  → GitHub Pages (relics.tracker.com)
```

---

## 使用方式

### 本地预览

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

### 网页端编辑

1. 打开 `https://relics.tracker.com`
2. 展开子系统，直接编辑任务字段
3. 修改保存在浏览器 localStorage
4. 点击 **Export JSON** 导出
5. 将导出的 JSON 更新到仓库 `data/commission.json`

### 推送到 GitHub

1. 点击 **Push to GitHub** 按钮
2. 填写 GitHub Token (PAT) 和仓库信息
3. 保存配置后点击 **Push Now**

### 生成 CODEOWNERS

1. 在各子系统头部编辑 GitHub 用户名
2. 点击 **CODEOWNERS** 按钮下载
3. 替换 `.github/CODEOWNERS` 文件
4. 提交到仓库

---

## 自定义域名配置

### DNS 设置（在域名服务商添加）

```
类型    主机记录    值
A       @          185.199.108.153
A       @          185.199.109.153
A       @          185.199.110.153
A       @          185.199.111.153
CNAME   www        yangjijun1992.github.io
```

### GitHub 设置

1. 仓库 Settings → Pages → Custom domain: `relics.tracker.com`
2. 勾选 **Enforce HTTPS**
3. DNS 生效后访问 `https://relics.tracker.com`

---

## 相关文件说明

| 文件 | 用途 |
|------|------|
| `index.html` | 单文件 SPA 仪表盘，含 HTML/CSS/JS |
| `data/commission.json` | 核心进度数据，所有子系统和任务 |
| `CNAME` | GitHub Pages 自定义域名配置 |
| `.github/CODEOWNERS` | 代码审核权限，按文件路径指定 reviewer |
| `.github/workflows/deploy.yml` | GitHub Actions 自动部署工作流 |
| `tpc_related/` | TPC 参考资料（Jupyter Notebook、甘特图），已 gitignore |
| `.gitignore` | 忽略 tpc_related/、__pycache__/、.DS_Store 等 |
