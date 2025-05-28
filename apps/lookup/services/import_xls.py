import openpyxl
from apps.lookup.models import Category, Material
from contextlib import closing


class ImportService:

    @staticmethod
    def import_xls(file) -> str:
        excel_mime_types = {
            'application/vnd.ms-excel',  # .xls
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        }
        if not any(file.content_type == mime for mime in excel_mime_types):
            return str('Файл не является Excel таблицей')
        try:
            with closing(openpyxl.load_workbook(file, read_only=True)) as excel_file:

                sheet = excel_file.active
                max_rows = sheet.max_row

                errors_array = []
                values = [tuple(sheet[row][col].value for col in range(6)) for row in range(2, max_rows + 1)]
                for index, value in enumerate(values):
                    code_cat = value[0]  # Код категории
                    name_cat = value[1]  # Имя категории
                    parent_cat = value[2]  # Род. категория
                    code_mat = value[3]  # Код материала
                    name_mat = value[4]  # Имя материала
                    cost = value[5]  # Стоимость

                    if (not name_cat or not code_cat) and index + 2 < max_rows:
                        errors_array.append(f"Товар или раздел пропущен на след строчке: {index + 2}")

                    if name_cat and code_cat:
                        parent_cat_obj = None
                        parent_cat_obj = Category.objects.filter(name=parent_cat).first()
                        category, _ = Category.objects.update_or_create(
                            code=code_cat,
                            defaults={
                                'name': name_cat,
                                'parent_cat': parent_cat_obj
                            }
                        )
                    if code_mat and name_mat and cost:
                        cat_obj = Category.objects.filter(name=name_cat).first()
                        Material.objects.update_or_create(
                            code=code_mat,
                            defaults={
                                'name': name_mat,
                                'cat': cat_obj,
                                'cost': cost
                            }
                        )
            if errors_array:
                return f'import done not fully but: {",".join(errors_array)}'
            return 'import done'

        except Exception as e:
            return str(e)
