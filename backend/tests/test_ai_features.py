"""
AI功能测试脚本

测试：
1. AI生成详细行程
2. AI优化行程
3. AI重新生成行程
"""

import requests
import time
import json
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

def login_and_get_token():
    """登录并获取token"""
    url = f"{BASE_URL}/api/v1/auth/login"
    data = {
        "email": "test@wanderflow.com",
        "password": "test123456"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ 登录失败: {response.status_code}")
        return None

def create_itinerary(token):
    """创建测试行程"""
    url = f"{BASE_URL}/api/v1/planner/generate"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "杭州3日游",
        "destination": "杭州",
        "days": 3,
        "budget": 4000,
        "travel_style": "leisure",
        "use_strict_json": True
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        itinerary = response.json()
        print(f"✅ 行程创建成功 (ID: {itinerary['id']})")
        return itinerary
    else:
        print(f"❌ 创建行程失败: {response.status_code}")
        print(response.text)
        return None

def test_generate_detail(token, itinerary_id):
    """测试AI生成详细行程"""
    print("\n" + "="*60)
    print("测试 1: AI生成详细行程")
    print("="*60)

    url = f"{BASE_URL}/api/v1/planner/itineraries/{itinerary_id}/generate-detail"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"use_strict_json": True}

    print("⏳ 正在生成详细行程，请稍候...")
    start_time = time.time()

    response = requests.post(url, json=data, headers=headers)
    elapsed_time = time.time() - start_time

    if response.status_code == 200:
        result = response.json()
        print(f"✅ 详细行程生成成功 (耗时: {elapsed_time:.1f}秒)")
        print(f"   - 标题: {result.get('title')}")
        print(f"   - 概述: {result.get('summary', 'N/A')[:50]}...")
        print(f"   - 亮点: {len(result.get('highlights', []))}条")
        print(f"   - 天数: {len(result.get('days_detail', []))}天")
        print(f"   - 实际花费: ¥{result.get('actual_cost', 'N/A')}")
        return True
    else:
        print(f"❌ 生成详细行程失败: {response.status_code}")
        print(response.text)
        return False

def test_optimize(token, itinerary_id):
    """测试AI优化行程"""
    print("\n" + "="*60)
    print("测试 2: AI优化行程")
    print("="*60)

    url = f"{BASE_URL}/api/v1/planner/itineraries/{itinerary_id}/optimize"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "feedback": "我想增加一些户外活动，比如骑行和徒步",
        "affected_days": [],
        "use_strict_json": True
    }

    print("⏳ 正在优化行程，请稍候...")
    start_time = time.time()

    response = requests.post(url, json=data, headers=headers)
    elapsed_time = time.time() - start_time

    if response.status_code == 200:
        result = response.json()
        print(f"✅ 行程优化成功 (耗时: {elapsed_time:.1f}秒)")
        print(f"   - 标题: {result.get('title')}")
        print(f"   - 概述: {result.get('summary', 'N/A')[:50]}...")
        print(f"   - 天数: {len(result.get('days_detail', []))}天")
        return True
    else:
        print(f"❌ 优化行程失败: {response.status_code}")
        print(response.text)
        return False

def test_regenerate(token):
    """测试AI重新生成行程"""
    print("\n" + "="*60)
    print("测试 3: AI重新生成行程")
    print("="*60)

    # 创建一个新行程用于重新生成
    itinerary = create_itinerary(token)
    if not itinerary:
        return False

    itinerary_id = itinerary['id']

    # 等待一下，确保AI生成完成
    time.sleep(2)

    url = f"{BASE_URL}/api/v1/planner/itineraries/{itinerary_id}/generate-detail"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"use_strict_json": True}

    print("⏳ 正在重新生成行程，请稍候...")
    start_time = time.time()

    response = requests.post(url, json=data, headers=headers)
    elapsed_time = time.time() - start_time

    if response.status_code == 200:
        result = response.json()
        print(f"✅ 重新生成行程成功 (耗时: {elapsed_time:.1f}秒)")
        print(f"   - 标题: {result.get('title')}")
        print(f"   - 天数: {len(result.get('days_detail', []))}天")
        return True
    else:
        print(f"❌ 重新生成失败: {response.status_code}")
        print(response.text)
        return False

def main():
    print("="*60)
    print("AI功能测试")
    print("="*60)

    # 1. 登录
    print("\n步骤 1: 登录")
    print("-"*60)
    token = login_and_get_token()
    if not token:
        return

    # 2. 创建行程
    print("\n步骤 2: 创建测试行程")
    print("-"*60)
    itinerary = create_itinerary(token)
    if not itinerary:
        return

    itinerary_id = itinerary['id']

    # 等待基础行程创建完成
    time.sleep(1)

    # 3. 测试AI生成详细行程
    success1 = test_generate_detail(token, itinerary_id)

    # 4. 测试AI优化行程
    success2 = test_optimize(token, itinerary_id)

    # 5. 测试AI重新生成行程
    success3 = test_regenerate(token)

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"AI生成详细行程: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"AI优化行程: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"AI重新生成行程: {'✅ 通过' if success3 else '❌ 失败'}")

    all_passed = success1 and success2 and success3
    print(f"\n整体结果: {'✅ 所有测试通过' if all_passed else '❌ 部分测试失败'}")

if __name__ == "__main__":
    main()
