"""
查看数据库中的中文数据
"""
import asyncio
import sys
from pathlib import Path

# Windows UTF-8编码支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import aiomysql
import json


async def show_chinese_activities():
    """以中文显示activities数据"""
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Zhuqing5201314',
        db='wanderflow_db',
        charset='utf8mb4',
        autocommit=True
    )

    cursor = await conn.cursor()

    # 查询数据
    await cursor.execute('''
        SELECT id, day_number, title, activities
        FROM itinerary_days
        ORDER BY itinerary_id, day_number
        LIMIT 3
    ''')

    print("=" * 80)
    print("数据库中的activities字段（中文显示）")
    print("=" * 80)

    async for row in cursor:
        day_id, day_num, title, activities_json = row

        print(f"\n【第{day_num}天】{title}")
        print("-" * 60)

        try:
            activities = json.loads(activities_json)

            for i, act in enumerate(activities[:5], 1):  # 只显示前5个活动
                print(f"\n  {i}. {act.get('title', '未命名')} ({act.get('time', '')})")
                print(f"     类型: {act.get('type', 'N/A')}")
                print(f"     时长: {act.get('duration', 'N/A')}")

                # 显示亮点
                if act.get('highlights'):
                    print(f"     亮点:")
                    for highlight in act['highlights'][:2]:
                        print(f"       • {highlight}")

                # 显示价格
                if act.get('ticket_price') is not None:
                    print(f"     门票: ¥{act['ticket_price']}")
                if act.get('average_cost'):
                    print(f"     人均: ¥{act['average_cost']}")

            if len(activities) > 5:
                print(f"\n  ... 还有 {len(activities) - 5} 个活动")

        except json.JSONDecodeError as e:
            print(f"  [解析错误] {e}")

    print("\n" + "=" * 80)

    # 检查表字符集
    await cursor.execute('''
        SELECT
            TABLE_NAME,
            TABLE_COLLATION,
            TABLE_COMMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = 'wanderflow_db'
        AND TABLE_NAME IN ('itineraries', 'itinerary_days')
    ''')

    print("\n表字符集配置:")
    print("-" * 60)
    async for row in cursor:
        print(f"{row[0]}: {row[1]}")

    print("\n" + "=" * 80)
    print("\n说明：")
    print("1. 数据库存储是正常的JSON格式")
    print("2. 在MySQL客户端中显示为\\uXXXX是正常的（Unicode转义）")
    print("3. 应用程序读取时会自动转换为中文")
    print("4. 如果要在MySQL客户端中直接看中文，使用：")
    print("   SELECT JSON_UNQUOTE(activities) FROM itinerary_days;")
    print("=" * 80)

    await cursor.close()
    conn.close()


if __name__ == "__main__":
    asyncio.run(show_chinese_activities())
