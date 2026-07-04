import pandas as pd
# Проверка реального места в направлении "Математика и компьютерные науки"

math_path = "1.csv"
biz_path = "2.csv"


biz = pd.read_csv(biz_path, sep=';', encoding='utf-8-sig')
math = pd.read_csv(math_path, sep=';', encoding='utf-8-sig')



qualifying = biz[
    (biz['Приоритет конкурса'] == 1) &
    (biz['Порядковый номер'] <= 111)
]
ids_to_remove = set(qualifying['Код поступающего'])

print(f"Найдено абитуриентов, попадающих под условие: {len(ids_to_remove)}")


math_filtered = math[~math['Код поступающего'].isin(ids_to_remove)].copy()


math_filtered = math_filtered.sort_values('Порядковый номер').reset_index(drop=True)
math_filtered['Новое место'] = range(1, len(math_filtered) + 1)


target_id = 1280590
result = math_filtered[math_filtered['Код поступающего'] == target_id]

if not result.empty:
    old_pos = result['Порядковый номер'].values[0]
    new_pos = result['Новое место'].values[0]
    print(f"ID {target_id}: было место {old_pos}, стало место {new_pos}")
else:
    print(f"ID {target_id} был удалён из списка (или не найден)")


# math_filtered.to_csv("Математика_пересчитано.csv", sep=';', index=False, encoding='utf-8-sig')