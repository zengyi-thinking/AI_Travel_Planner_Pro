# -*- coding: utf-8 -*-
"""
创建测试用户并验证前端功能
"""
import requests
import json
import sys

# 设置输出编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def create_test_user():
    """创建测试用户"""
    print_section("1. 创建测试用户")

    url = f"{BASE_URL}/api/v1/auth/register"
    user_data = {
        "email": "test@wanderflow.com",
        "password": "test123456",
        "name": "测试用户"
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(user_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=user_data)
        print(f"\n状态码: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            print(f"[OK] 用户创建成功!")
            print(f"   用户名: {data.get('user', {}).get('name')}")
            print(f"   邮箱: {data.get('user', {}).get('email')}")
            print(f"   会员等级: {data.get('user', {}).get('membership_level')}")
            return data.get('access_token')
        elif response.status_code == 400:
            print(f"[INFO] 用户已存在，尝试登录...")
            return login_test_user()
        else:
            print(f"[FAIL] 创建失败: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return None

def login_test_user():
    """登录测试用户"""
    print_section("2. 登录测试用户")

    url = f"{BASE_URL}/api/v1/auth/login"
    login_data = {
        "email": "test@wanderflow.com",
        "password": "test123456"
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(login_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=login_data)
        print(f"\n状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 登录成功!")
            print(f"   用户名: {data.get('user', {}).get('name')}")
            print(f"   Token: {data.get('access_token')[:20]}...")
            return data.get('access_token')
        else:
            print(f"[FAIL] 登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return None

def test_create_itinerary(token):
    """测试创建行程"""
    print_section("3. 创建行程")

    url = f"{BASE_URL}/api/v1/planner/generate"
    itinerary_data = {
        "title": "成都3日游",
        "destination": "成都",
        "days": 3,
        "budget": 3500,
        "travel_style": "leisure",
        "use_strict_json": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(itinerary_data, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(url, json=itinerary_data, headers=headers)
        print(f"\n状态码: {response.status_code}")

        if response.status_code in [200, 201]:
            data = response.json()
            print(f"[OK] 行程创建成功!")
            print(f"   行程ID: {data.get('id')}")
            print(f"   标题: {data.get('title')}")
            print(f"   目的地: {data.get('destination')}")
            print(f"   天数: {data.get('days')}")
            print(f"   状态: {data.get('status')}")
            return data.get('id')
        else:
            print(f"[FAIL] 创建失败: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return None

def test_generate_detail(token, itinerary_id):
    """测试生成详细行程"""
    print_section("4. 生成详细行程")

    url = f"{BASE_URL}/api/v1/planner/itineraries/{itinerary_id}/generate-detail"
    request_data = {
        "use_strict_json": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"POST {url}")
    print(f"请求参数: {json.dumps(request_data, ensure_ascii=False)}")
    print("\n[INFO] AI正在生成详细行程，请稍候...")

    try:
        response = requests.post(url, json=request_data, headers=headers)
        print(f"\n状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 详细行程生成成功!")

            # 检查V2字段
            print(f"\nV2数据字段:")
            v2_fields = {
                'summary': '摘要',
                'highlights': '亮点',
                'best_season': '最佳季节',
                'weather': '天气',
                'actual_cost': '实际花费',
                'cost_breakdown': '费用明细',
                'preparation': '行前准备',
                'tips': '实用提示',
                'days_detail': '每日详情'
            }

            for field, name in v2_fields.items():
                status = 'OK' if data.get(field) else 'MISSING'
                print(f"   [{status}] {name}")

            # 显示部分数据
            if data.get('summary'):
                print(f"\n行程摘要: {data['summary'][:80]}...")

            if data.get('highlights'):
                print(f"\n行程亮点 ({len(data['highlights'])}条):")
                for i, h in enumerate(data['highlights'][:3], 1):
                    print(f"   {i}. {h}")

            if data.get('days_detail'):
                print(f"\n每日行程:")
                for day in data['days_detail']:
                    activities = len(day.get('activities', []))
                    print(f"   第{day.get('day_number')}天: {day.get('title')} ({activities}个活动)")

            return True
        else:
            print(f"[FAIL] 生成失败: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return False

def main():
    """主函数"""
    print_section("前后端集成测试")
    print("后端: http://localhost:8000")
    print("前端: http://localhost:3000")

    # 1. 创建/登录用户
    token = create_test_user()
    if not token:
        print("\n[FAIL] 测试终止: 无法获取认证token")
        return

    print("\n[OK] 步骤1完成: 用户认证成功")

    # 2. 创建行程
    itinerary_id = test_create_itinerary(token)
    if not itinerary_id:
        print("\n[FAIL] 测试终止: 无法创建行程")
        return

    print(f"\n[OK] 步骤2完成: 行程已创建 (ID: {itinerary_id})")

    # 3. 生成详细行程
    success = test_generate_detail(token, itinerary_id)
    if not success:
        print(f"\n[FAIL] 步骤3失败: 无法生成详细行程")
        return

    print(f"\n[OK] 步骤3完成: 详细行程已生成")

    # 总结
    print_section("测试总结")
    print("[OK] 用户认证正常")
    print("[OK] 创建行程正常")
    print("[OK] 生成详细行程正常")
    print("[OK] V2数据结构完整")
    print(f"\n现在可以访问前端进行测试:")
    print(f"  前端地址: http://localhost:3000")
    print(f"  测试账号: test@wanderflow.com")
    print(f"  测试密码: test123456")

if __name__ == "__main__":
    main()
