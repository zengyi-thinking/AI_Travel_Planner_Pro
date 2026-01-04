import asyncio
import json
from sqlalchemy import text
from app.core.db.session import get_db

async def check_coords():
    async for db in get_db():
        # 查询行程100的活动
        result = await db.execute(text('''
            SELECT activities
            FROM day_details 
            WHERE itinerary_id = 100
            LIMIT 1
        '''))
        row = result.fetchone()
        if row:
            activities = json.loads(row[0])
            print(f'第一天活动数: {len(activities)}')
            has_coords_count = 0
            for i, act in enumerate(activities[:5], 1):
                coords = act.get('coordinates')
                if coords:
                    has_coords_count += 1
                    print(f'  {i}. {act.get("title")}: 有坐标 ({coords.get("lat")}, {coords.get("lng")})')
                else:
                    print(f'  {i}. {act.get("title")}: 无坐标')
            
            if has_coords_count == 0:
                print('\n结论: 数据库中没有任何坐标数据！')
                print('这证明后端的坐标获取功能确实没有被执行。')
        break

asyncio.run(check_coords())
