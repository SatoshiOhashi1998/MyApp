import xlwings as xw


def update_excel(file_path, sheet_name, new_data):
    """
    Excelファイルを開き、指定されたシートにデータを追加する関数

    :param file_path: Excelファイルのパス
    :param sheet_name: 対象のシート名
    :param new_data: 追加する新しいデータ（タプル形式）
    """
    app = xw.App(visible=False)
    wb = None
    try:
        wb = app.books.open(file_path)
        sheet = wb.sheets[sheet_name]

        # B列のデータが空でない最終行を取得（空なら1行目から）
        if sheet.range('B2').value is None:
            last_row = 1
        else:
            last_row = sheet.range('B2').end('down').row

        # データを追加
        sheet.range(f'B{last_row + 1}:D{last_row + 1}').value = new_data

        # 保存
        wb.save()

        # 追加したデータの確認
        start_row = 2 if sheet.range('B2').value else last_row + 1
        for row in sheet.range(f'B{start_row}:D{last_row + 1}').value:
            print(row)

    finally:
        if wb:
            wb.close()
        app.quit()


def update_excel_multiple(file_path, sheet_name, new_data_list):
    """
    Excelファイルを開き、指定されたシートに複数のデータを追加する関数

    :param file_path: Excelファイルのパス
    :param sheet_name: 対象のシート名
    :param new_data_list: 追加する新しいデータのリスト（タプルのリスト）
    """
    app = xw.App(visible=False)
    wb = None
    try:
        wb = app.books.open(file_path)
        sheet = wb.sheets[sheet_name]

        # B列のデータが空でない最終行を取得（空なら1行目から）
        if sheet.range('B2').value is None:
            last_row = 1
        else:
            last_row = sheet.range('B2').end('down').row

        # 複数データを順番に追加
        for new_data in new_data_list:
            sheet.range(f'B{last_row + 1}:D{last_row + 1}').value = new_data
            last_row += 1  # 行を更新

        # 保存
        wb.save()

        # 追加したデータの確認
        start_row = 2 if sheet.range('B2').value else last_row - len(new_data_list) + 1
        for row in sheet.range(f'B{start_row}:D{last_row}').value:
            print(row)

    finally:
        if wb:
            wb.close()
        app.quit()


# 使用例：
# file_path = r"C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\static\excel\test.xlsm"
file_path = r"C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\excel\streaming_data.xlsx"
sheet_name = '2025年上半期'
new_data_list = [
    ("腹筋割れてます", "一ノ瀬うるは", "昔から", "エロサイト"),
    ("腹筋割れてます", "胡桃のあ", "昔から", "エロサイト"),
]

# 関数を呼び出して複数のデータを追加
update_excel_multiple(file_path, sheet_name, new_data_list)
