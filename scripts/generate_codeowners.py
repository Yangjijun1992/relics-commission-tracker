#!/usr/bin/env python3
"""
Generate CODEOWNERS file from commission.json
"""

import json
import sys
from pathlib import Path

def generate_codeowners(json_path: Path, output_path: Path) -> bool:
    """Generate CODEOWNERS file from commission.json data."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}", file=sys.stderr)
        return False

    lines = [
        "# RELICS Commission Tracker - CODEOWNERS",
        "# 自动生成 - 基于 commission.json 中的 github_user 字段",
        "# 详细说明: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners",
        "#",
        "# ⚠️ 待办: 收集各子系统负责人的 GitHub 用户名后，更新 commission.json 中的 github_user 字段，",
        "#    然后在网页端点击 \"CODEOWNERS\" 按钮重新生成此文件。",
        "",
        "# ============================================================",
        "# 项目级管理员（所有变更必须经过审核）",
        "# ============================================================",
        "*                                   @Yangjijun1992",
        "",
        "# ============================================================",
        "# 核心数据文件",
        "# ============================================================",
        "/data/commission.json                @Yangjijun1992",
        "/index.html                         @Yangjijun1992",
        "",
        "# ============================================================",
        "# 子系统负责人（基于 github_user 字段）",
        "# ============================================================",
    ]

    for subsystem in data.get('subsystems', []):
        subsystem_id = subsystem.get('id', 'unknown')
        name = subsystem.get('name', 'Unknown')
        name_cn = subsystem.get('name_cn', '未知')
        responsible = subsystem.get('responsible', '未知')
        github_user = subsystem.get('github_user', '')

        if github_user:
            lines.append(f"\n# {subsystem_id.upper()} - {name_cn}（负责人: {responsible}）")
            lines.append(f"/data/commission.json                @{github_user}")
        else:
            lines.append(f"\n# {subsystem_id.upper()} - {name_cn}（负责人: {responsible}）⚠️ 待填写")
            lines.append(f"# @TBD-{subsystem_id}")

    lines.extend([
        "",
        "# ============================================================",
        "# 部署相关文件（仅管理员可修改）",
        "# ============================================================",
        "/.github/                            @Yangjijun1992",
        "/CNAME                               @Yangjijun1992",
        "",
    ])

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"CODEOWNERS generated successfully at {output_path}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    json_path = script_dir.parent / "data" / "commission.json"
    output_path = script_dir.parent / ".github" / "CODEOWNERS"

    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    success = generate_codeowners(json_path, output_path)
    sys.exit(0 if success else 1)
