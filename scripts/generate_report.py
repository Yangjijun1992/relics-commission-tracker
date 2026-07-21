#!/usr/bin/env python3
"""
Generate progress report from commission.json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def generate_report(json_path: Path) -> str:
    """Generate a Markdown progress report from commission.json."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}", file=sys.stderr)
        return ""

    lines = []
    lines.append(f"# {data['project']['name']} - 进度报告")
    lines.append(f"")
    lines.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**项目周期:** {data['project']['start_date']} ~ {data['project']['end_date']}")
    lines.append(f"**负责人:** {data['project']['pi']}")
    lines.append(f"")

    # Overall statistics
    total_tasks = 0
    completed = 0
    in_progress = 0
    not_started = 0
    delayed = 0
    total_progress = 0

    for subsystem in data['subsystems']:
        for task in subsystem['subtasks']:
            total_tasks += 1
            total_progress += task['progress']
            if task['status'] == 'completed':
                completed += 1
            elif task['status'] == 'in_progress':
                in_progress += 1
            elif task['status'] == 'not_started':
                not_started += 1
            elif task['status'] == 'delayed':
                delayed += 1

    overall_progress = total_progress // total_tasks if total_tasks > 0 else 0

    lines.append(f"## 总体统计")
    lines.append(f"")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总任务数 | {total_tasks} |")
    lines.append(f"| 已完成 | {completed} ({completed*100//total_tasks}%) |")
    lines.append(f"| 进行中 | {in_progress} ({in_progress*100//total_tasks}%) |")
    lines.append(f"| 未开始 | {not_started} ({not_started*100//total_tasks}%) |")
    lines.append(f"| 延迟 | {delayed} ({delayed*100//total_tasks}%) |")
    lines.append(f"| 总体进度 | {overall_progress}% |")
    lines.append(f"")

    # Subsystem details
    lines.append(f"## 子系统详情")
    lines.append(f"")

    for subsystem in data['subsystems']:
        sys_progress = 0
        if subsystem['subtasks']:
            sys_progress = sum(t['progress'] for t in subsystem['subtasks']) // len(subsystem['subtasks'])

        lines.append(f"### {subsystem['name_cn']} ({subsystem['name']})")
        lines.append(f"")
        lines.append(f"- **负责人:** {subsystem['responsible']}")
        lines.append(f"- **计划周期:** {subsystem['planned_start']} ~ {subsystem['planned_end']}")
        lines.append(f"- **进度:** {sys_progress}%")
        lines.append(f"- **任务数量:** {len(subsystem['subtasks'])}")
        lines.append(f"")

        # Task list
        lines.append(f"| ID | 任务名称 | 负责人 | 状态 | 进度 | 计划结束 |")
        lines.append(f"|-----|----------|--------|------|------|----------|")

        for task in subsystem['subtasks']:
            status_emoji = {
                'not_started': '⬜',
                'in_progress': '🔄',
                'completed': '✅',
                'delayed': '⚠️',
                'cancelled': '❌'
            }.get(task['status'], '❓')

            lines.append(f"| {task['id']} | {task['name_cn']} | {task['assignee']} | {status_emoji} {task['status']} | {task['progress']}% | {task['planned_end']} |")

        lines.append(f"")

    # Key milestones
    lines.append(f"## 关键里程碑")
    lines.append(f"")

    today = datetime.now()
    upcoming_milestones = []

    for subsystem in data['subsystems']:
        for task in subsystem['subtasks']:
            if task['status'] != 'completed':
                try:
                    end_date = datetime.strptime(task['planned_end'], '%Y-%m-%d')
                    days_remaining = (end_date - today).days
                    if 0 <= days_remaining <= 30:
                        upcoming_milestones.append({
                            'task': task,
                            'subsystem': subsystem,
                            'days_remaining': days_remaining
                        })
                except ValueError:
                    pass

    upcoming_milestones.sort(key=lambda x: x['days_remaining'])

    if upcoming_milestones:
        lines.append(f"**未来30天内到期的任务:**")
        lines.append(f"")
        for item in upcoming_milestones[:10]:  # Show top 10
            task = item['task']
            subsystem = item['subsystem']
            days = item['days_remaining']
            urgency = "🔴" if days <= 7 else "🟡" if days <= 14 else "🟢"
            lines.append(f"- {urgency} **{task['name_cn']}** ({subsystem['name_cn']}) - 还有 {days} 天到期")
        lines.append(f"")
    else:
        lines.append(f"未来30天内没有即将到期的任务。")
        lines.append(f"")

    # Action items
    lines.append(f"## 待办事项")
    lines.append(f"")

    action_items = []
    for subsystem in data['subsystems']:
        for task in subsystem['subtasks']:
            if task['status'] == 'delayed':
                action_items.append(f"- ⚠️ **{task['name_cn']}** ({subsystem['name_cn']}) 已延迟，需要关注")
            elif task['status'] == 'in_progress' and task['progress'] < 50:
                action_items.append(f"- 🔄 **{task['name_cn']}** ({subsystem['name_cn']}) 进度较慢 ({task['progress']}%)")

    if action_items:
        lines.extend(action_items[:10])  # Show top 10
    else:
        lines.append(f"暂无需要特别关注的事项。")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*报告由 RELICS Commission Tracker 自动生成*")

    return '\n'.join(lines)

def main():
    script_dir = Path(__file__).parent
    json_path = script_dir.parent / "data" / "commission.json"
    output_path = script_dir.parent / "progress_report.md"

    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    report = generate_report(json_path)
    if not report:
        print("Error: Failed to generate report", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Progress report generated successfully at {output_path}")
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
