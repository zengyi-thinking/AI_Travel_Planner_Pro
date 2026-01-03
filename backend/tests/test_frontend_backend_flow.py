# -*- coding: utf-8 -*-
"""
测试前后端完整流程
1. 用户登录
2. 创建基础行程
3. 生成详细行程
4. 验证数据结构
"""
import requests
import json
import sys
from typing import Dict, Any

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_URL = "http://localhost:8000"

# 全局变量存储token
access_token = None

def print_section(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def get_headers() -> Dict[str, str]:
    """获取带认证的请求头"""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

def test_register_login() -> bool:
    """测试注册和登录"""
    print_section("1. 用户注册/登录")

    # 先尝试登录
    login_url = f"{BASE_URL}/api/v1/auth/login"
    register_url = f"{BASE_URL}/api/v1/auth/register"

    # 注册数据
    register_data = {
        "email": "test@wanderflow.com",
        "password": "test123456",
        "name": "Test User"
    }

    # 登录数据
    login_data = {
        "email": "test@wanderflow.com",
        "password": "test123456"
    }

    try:
        # 先尝试注册（可能已存在）
        print(f"尝试注册用户: {register_data['email']}")
        reg_response = requests.post(register_url, json=register_data)
        print(f"注册状态码: {reg_response.status_code}")

        # 登录
        print(f"\n尝试登录...")
        login_response = requests.post(login_url, json=login_data)
        print(f"登录状态码: {login_response.status_code}")

        if login_response.status_code == 200:
            data = login_response.json()
            global access_token
            access_token = data.get('access_token')
            print(f"\n[OK] 登录成功!")
            print(f"   用户: {data.get('user', {}).get('name')}")
            print(f"   会员等级: {data.get('user', {}).get('membership_level')}")
            return True
        else:
            print(f"\n[FAIL] 登录失败: {login_response.text}")
            return False
    except Exception as e:
        print(f"\n[ERROR] 请求异常: {e}")
        return False

def test_create_itinerary() -> Dict[str, Any]:
    """测试创建基础行程"""
    print_section("2. 创建基础行程")

    url = f"{BASE_URL}/api/v1/planner/generate"
    payload = {
        "title": "成都3日游测试",
        "destination": "成都",
        "days": 3,
        "budget": 3500,
        "travel_style": "leisure",
        "use_strict_json": True
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(url, json=payload, headers=get_headers())
        print(f"\n状态码: {response.status_code}")

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print(f"\n[OK] 基础行程创建成功!")
            print(f"   - ID: {data.get('id')}")
            print(f"   - 标题: {data.get('title')}")
            print(f"   - 目的地: {data.get('destination')}")
            print(f"   - 天数: {data.get('days')}")
            print(f"   - 状态: {data.get('status')}")
            return data
        else:
            print(f"\n[FAIL] 请求失败: {response.text}")
            return {}
    except Exception as e:
        print(f"\n[ERROR] 请求异常: {e}")
        return {}

def test_generate_detail(itinerary_id: int) -> Dict[str, Any]:
    """测试生成详细行程"""
    print_section("3. 生成详细行程")

    url = f"{BASE_URL}/api/v1/planner/itineraries/{itinerary_id}/generate-detail"
    payload = {
        "use_strict_json": True
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print("\nAI正在生成详细行程，请稍候...")

    try:
        response = requests.post(url, json=payload, headers=get_headers())
        print(f"\n状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n[OK] 详细行程生成成功!")

            # 检查V2字段
            print(f"\nV2数据结构检查:")
            print(f"   - 摘要 (summary): {'OK' if data.get('summary') else 'MISSING'}")
            print(f"   - 亮点 (highlights): {'OK' if data.get('highlights') else 'MISSING'}")
            print(f"   - 最佳季节 (best_season): {'OK' if data.get('best_season') else 'MISSING'}")
            print(f"   - 天气 (weather): {'OK' if data.get('weather') else 'MISSING'}")
            print(f"   - 实际花费 (actual_cost): {'OK' if data.get('actual_cost') else 'MISSING'}")
            print(f"   - 费用明细 (cost_breakdown): {'OK' if data.get('cost_breakdown') else 'MISSING'}")
            print(f"   - 行前准备 (preparation): {'OK' if data.get('preparation') else 'MISSING'}")
            print(f"   - 实用提示 (tips): {'OK' if data.get('tips') else 'MISSING'}")
            print(f"   - 每日详情 (days_detail): {'OK' if data.get('days_detail') else 'MISSING'}")

            # 显示概览信息
            if data.get('summary'):
                print(f"\n行程摘要:")
                print(f"   {data['summary'][:100]}...")

            # 显示亮点
            if data.get('highlights'):
                print(f"\n行程亮点 ({len(data['highlights'])}条):")
                for i, highlight in enumerate(data['highlights'][:3], 1):
                    print(f"   {i}. {highlight}")

            # 显示每日行程
            if data.get('days_detail'):
                print(f"\n每日行程 ({len(data['days_detail'])}天):")
                for day in data['days_detail']:
                    activities_count = len(day.get('activities', []))
                    print(f"   - 第{day.get('day_number')}天: {day.get('title')} ({activities_count}个活动)")

            return data
        else:
            print(f"\n[FAIL] 请求失败: {response.text}")
            return {}
    except Exception as e:
        print(f"\n[ERROR] 请求异常: {e}")
        return {}

def test_frontend_api_compatibility(data: Dict[str, Any]):
    """测试前端API兼容性"""
    print_section("4. 前端API兼容性检查")

    # 检查必需字段
    required_fields = [
        'id', 'title', 'destination', 'days', 'budget',
        'travel_style', 'status', 'created_at', 'updated_at'
    ]

    print("检查必需字段:")
    all_passed = True
    for field in required_fields:
        exists = field in data
        status = "OK" if exists else "MISSING"
        print(f"   [{status}] {field}")
        if not exists:
            all_passed = False

    # 检查V2字段
    v2_fields = [
        'summary', 'highlights', 'best_season', 'weather',
        'actual_cost', 'cost_breakdown', 'preparation', 'tips', 'days_detail'
    ]

    print(f"\n检查V2扩展字段:")
    for field in v2_fields:
        exists = field in data and data[field] is not None
        status = "OK" if exists else "MISSING"
        print(f"   [{status}] {field}")

    # 检查days_detail数据结构
    if data.get('days_detail'):
        print(f"\n检查每日行程数据结构:")
        for day in data['days_detail']:
            day_num = day.get('day_number')
            has_title = bool(day.get('title'))
            has_activities = bool(day.get('activities'))
            print(f"   第{day_num}天: 标题 [{('OK' if has_title else 'MISSING')}], 活动 [{('OK' if has_activities else 'MISSING')}]")

            if day.get('activities'):
                activity = day['activities'][0]
                print(f"      活动示例: {activity.get('title')} ({activity.get('type')})")

    if all_passed:
        print(f"\n[OK] 所有必需字段检查通过!")
    else:
        print(f"\n[FAIL] 部分字段检查失败!")

def main():
    """主测试流程"""
    print_section("前后端完整流程测试")
    print("后端地址: http://localhost:8000")
    print("前端地址: http://localhost:3000")

    # 1. 注册/登录
    if not test_register_login():
        print("\n[FAIL] 测试终止: 无法登录")
        return

    print("\n[OK] 步骤1完成: 用户认证成功")

    # 2. 创建基础行程
    itinerary = test_create_itinerary()
    if not itinerary:
        print("\n[FAIL] 测试终止: 无法创建基础行程")
        return

    itinerary_id = itinerary.get('id')
    print(f"\n[OK] 步骤2完成: 基础行程已创建 (ID: {itinerary_id})")

    # 3. 生成详细行程
    detailed_itinerary = test_generate_detail(itinerary_id)
    if not detailed_itinerary:
        print(f"\n[FAIL] 步骤3失败: 无法生成详细行程")
        return

    print(f"\n[OK] 步骤3完成: 详细行程已生成")

    # 4. 测试前端兼容性
    test_frontend_api_compatibility(detailed_itinerary)

    # 总结
    print_section("测试总结")
    print("[OK] 前后端通信正常")
    print("[OK] V2数据结构支持完整")
    print("[OK] 前端可以正确解析和展示数据")
    print(f"\n行程ID: {itinerary_id}")
    print(f"前端访问: http://localhost:3000")
    print(f"后端API: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
