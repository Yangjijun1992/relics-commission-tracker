# RELICS Commission Run Tracker

实时跟踪 RELICS 实验 Commission Run 各子系统进度的 Web 仪表盘。

## 功能

- **子系统进度追踪** — 5 大子系统及其子任务的进度、状态、负责人
- **甘特图时间线** — 可视化各子任务的时间安排与完成情况
- **实时编辑** — 在网页上直接修改进度/状态/备注，自动保存到 localStorage
- **GitHub Pages** — push 到 main 分支后自动部署，组内成员通过 URL 即可访问

## 子系统

| Subsystem | Chinese | 说明 |
|-----------|---------|------|
| Photon Detection System | 光子探测系统 | PMT/SiPM 安装标定 |
| DAQ System | 数据采集系统 | 电子学、触发、采集软件 |
| TPC System | 时间投影室系统 | 场笼、气体、高压 |
| Computing System | 计算系统 | 离线处理、存储、批处理 |
| Cryogenics & Circulation | 低温与循环系统 | 冷却、循环、热稳定性 |

## 使用方式

### 本地预览

```bash
# 任意 HTTP 服务器均可
python3 -m http.server 8000
# 然后浏览器打开 http://localhost:8000
```

### 部署到 GitHub Pages

1. 创建 GitHub 仓库并推送代码
2. 进入仓库 Settings → Pages → Source 选择 `GitHub Actions`
3. 每次 push 到 `main` 分支会自动部署

### 修改进度数据

直接编辑 `data/commission.json`，或在网页界面上直接操作（进度滑块、状态下拉框、备注输入框）。

网页编辑的数据保存在浏览器 localStorage 中。如果需要持久化，将 JSON 导出后更新仓库。

## JSON 数据结构

```json
{
  "project": { "name", "description", "pi", "start_date", "end_date" },
  "subsystems": [
    {
      "id", "name", "name_cn", "responsible", "planned_start", "planned_end",
      "subtasks": [
        {
          "id", "name", "name_cn", "planned_start", "planned_end",
          "status": "not_started|in_progress|completed|blocked|delayed",
          "progress": 0-100,
          "assignee", "notes"
        }
      ]
    }
  ]
}
```

## 文件结构

```
relics_commission/
├── index.html              # 仪表盘主页
├── data/
│   └── commission.json     # 进度数据
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Pages 自动部署
└── README.md
```