# TODO - RELICS Commission Tracker 后续待办

> 创建日期：2026-07-19
> 最后更新：2026-07-19

---

## 高优先级

### 1. 启用 GitHub Pages 部署

- [x] 进入 https://github.com/Yangjijun1992/relics-commission-tracker/settings/pages
- [x] **Source** → 选择 `GitHub Actions`
- [x] 手动触发 `Deploy to GitHub Pages` workflow
- [x] 确认页面正常加载：**https://Yangjijun1992.github.io/relics-commission-tracker/**
- [x] 删除 CNAME 文件（暂不使用自定义域名）

### 2. 收集各子系统负责人 GitHub 用户名

- [x] 谢凌峰（TPC）→ 已填写 `LingFeng-Xie`
- [x] 王俊（Computing / Muon）→ 已填写 `elphen-wang`
- [ ] 于佳成（Cryo）→ 待填写
- [ ] 岳玉用（Shield）→ 待填写
- [ ] 陈江宇（Facilities）→ 待填写
- [ ] 蔡畅（DAQ）→ 待填写
- [ ] 雷阳（DAQ）→ 待填写
- [ ] 王笑宇（Muon）→ 待填写

**操作方式：** 在网页端各子系统头部的 `@TBD-xxx` 处直接编辑，或修改 `data/commission.json` 中的 `github_user` 字段，然后运行 `python scripts/generate_codeowners.py`。

### 2. GitHub 分支保护配置

- [ ] 进入仓库 Settings → Branches → Add branch protection rule
- [ ] Branch name pattern: `main`
- [ ] 勾选 **Require a pull request before merging**
- [ ] 勾选 **Require approvals**（至少 1 人）
- [ ] 勾选 **Require review from Code Owners**
- [ ] 勾选 **Do not allow bypassing the above settings**
- [ ] 测试：尝试直接 push main，确认被拒绝

### 4. 自定义域名 DNS 配置

- [ ] **确认域名注册商**（阿里云/腾讯云/Cloudflare/其他？联系实验室管理人员）
- [ ] 登录域名管理后台
- [ ] 添加 A 记录（4 条，指向 GitHub Pages IP）：
  ```
  类型    主机记录    值
  A       @          185.199.108.153
  A       @          185.199.109.153
  A       @          185.199.110.153
  A       @          185.199.111.153
  ```
- [ ] 添加 CNAME 记录：`www` → `yangjijun1992.github.io`
- [ ] 在 GitHub Pages 设置中填入 Custom domain: `relics.tracker.com`
- [ ] 勾选 **Enforce HTTPS**
- [ ] 等待 DNS 生效（几分钟 ~ 48 小时）
- [ ] 确认 `https://relics.tracker.com` 可访问

---

## 中优先级

### 5. 数据完善

- [ ] 为所有 `assignee: TBD` 的任务分配具体负责人
- [ ] 更新各任务的 `progress` 百分比（基于实际进展）
- [ ] 补充 `notes` 字段中的详细说明
- [ ] 检查并修正时间线冲突：
  - `cryo-01 冷却系统调试`(07-05) 在 `cryostat设计定制`(06-17~09-15) 完成之前就开始
  - `tpc-01 场笼组装`(07-10) 与 `TPC安装支架`(07-01~08-01) 时间重叠

### 6. 查看器功能增强

- [ ] 添加任务筛选/搜索功能（按名称、负责人、状态）
- [ ] 添加子系统筛选器（只显示特定子系统）
- [ ] 甘特图支持按子系统展开/折叠
- [ ] 甘特图添加"今天"标记线
- [ ] 导出功能支持 PDF 格式
- [ ] 移动端适配优化

### 7. 自动化增强

- [x] GitHub Action：自动从 commission.json 生成 CODEOWNERS (`generate-codeowners.yml`)
- [x] GitHub Action：PR 修改 commission.json 时自动检查数据格式 (`validate-commission.yml`)
- [x] GitHub Action：定时生成进度报告 (`generate-report.yml`)
- [ ] Webhook：任务状态变更时通知相关负责人

---

## 低优先级

### 8. 数据分析

- [ ] 添加关键路径分析（识别瓶颈任务）
- [ ] 添加资源冲突检测（同一负责人同时段任务过多）
- [ ] 添加里程碑依赖关系可视化
- [ ] 历史版本对比（diff 视图）

### 9. 多语言支持

- [ ] 查看器支持中英文切换
- [ ] 任务名称支持双语显示（当前已支持）

### 10. 文档完善

- [ ] 编写贡献者指南（CONTRIBUTING.md）
- [ ] 编写部署指南（针对新管理员）
- [ ] 编写子系统负责人操作手册

---

## 已完成

- [x] 创建 commission.json 数据结构（8 子系统）
- [x] 创建 index.html 仪表盘查看器
- [x] 创建 GitHub Actions 部署工作流
- [x] 合并 Jupyter Notebook TPC 任务（+17 项）
- [x] 修复 PDS pds-08 重复 ID
- [x] 添加 github_user 字段到各子系统
- [x] 创建 CODEOWNERS 模板
- [x] 实现 CODEOWNERS 生成功能（脚本 + Action）
- [x] 实现数据校验功能（脚本 + Action）
- [x] 实现进度报告生成（脚本 + Action）
- [x] GitHub Pages 部署成功
- [x] 更新 README.md

---

## 快速参考

### 文件修改入口

| 文件 | 用途 | 修改频率 |
|------|------|----------|
| `data/commission.json` | 核心数据 | 高（每次进度更新） |
| `.github/CODEOWNERS` | 权限配置 | 低（用户名变更时） |
| `CNAME` | 域名配置 | 极低 |
| `index.html` | 查看器 | 低（功能迭代时） |

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

# 提交并推送
git add data/commission.json && git commit -m "update: 进度更新" && git push origin main
```
