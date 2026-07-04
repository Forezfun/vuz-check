import pandas as pd
# Проверка реального места в направлении "Бизнес-информатика"

math_path = "1.csv"
biz_path = "2.csv"

biz = pd.read_csv(biz_path, sep=';', encoding='utf-8-sig')
math = pd.read_csv(math_path, sep=';', encoding='utf-8-sig')

my_id = 1280590      
threshold = 565



qualifying = math[
    (math['Приоритет конкурса'] == 1) &
    (math['Порядковый номер'] <= threshold)
]
ids_to_remove = set(qualifying['Код поступающего']) - {my_id}

print(f"Найдено в 'Математике и КН' с условием: {len(qualifying)}")
print(f"К удалению из 'Бизнес-информатики' (без меня): {len(ids_to_remove)}")


biz_filtered = biz[~biz['Код поступающего'].isin(ids_to_remove)].copy()


biz_filtered = biz_filtered.sort_values('Порядковый номер').reset_index(drop=True)
biz_filtered['Новое место'] = range(1, len(biz_filtered) + 1)


result = biz_filtered[biz_filtered['Код поступающего'] == my_id]
if not result.empty:
    old_pos = result['Порядковый номер'].values[0]
    new_pos = result['Новое место'].values[0]
    print(f"ID {my_id}: было место {old_pos}, стало место {new_pos}")
else:
    print(f"ID {my_id} не найден в списке 'Бизнес-информатика'")

# biz_filtered.to_csv("Бизнес-информатика_пересчитано.csv", sep=';', index=False, encoding='utf-8-sig')