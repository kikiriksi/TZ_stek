import os
import shutil
import aspose.pdf as ap

'''Перед запуском всей программы не должно быть папок "checks","sorted_directory","не оплачены"!!!!!!.
Программа читает название файлов из чеки.txt и создаёт файлы pdf в папку checks.
Далее создаёт папку sorted_directory и в ней папки с названием месяцев.
Сортирует файлы из папки checks и раскидывает по месяцам.
Следующий шаг создание папки "не оплачены" и проверяет каких чеков недостоёт в каждом месяце и создаёт их там в виде 
задолжности'''

months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
          'декабрь']

set_service = []


class Checks:
    def file_simulation(self):
        '''создает имитацию файлов pdf по названию в текстовом документе в папку checks для чеков'''
        os.mkdir('checks')
        with open('чеки.txt', mode='r', encoding='utf-8') as file:
            checks = file.readlines()
            for check in checks:
                document = ap.Document()
                page = document.pages.add()
                text_fragment = ap.text.TextFragment(check)
                page.paragraphs.add(text_fragment)
                document.save(f'checks/{check.strip()}')

    def new_catalog(self):
        '''Создаёт основную директорию для папок'''
        os.mkdir('sorted_directory')
        '''создаём папки с названием месяцев'''
        for month in months:
            os.mkdir(f'sorted_directory/{month}')

    def scan_directory_service(self):
        '''Создаёт список всех услуг и сохраняет в списке "set_service"'''
        services = [i.split('_')[0] for i in os.listdir('checks')]
        for service in services:
            for month in months:
                service = service.replace(f'_{month}', '')
                service = service.replace('\ufeff', '')
                if not service in set_service:
                    set_service.append(service)

    def scan_directory(self):
        '''сканирую папку со всеми чеками и по названию чека перемещаем в соответствующую по месяцу папку'''
        checks = os.listdir('checks')
        filter_directory = os.listdir('sorted_directory')
        for directory in filter_directory:
            for check in checks:
                if directory in check.strip():
                    shutil.move(f'checks\\{check}',
                                f'sorted_directory\\{directory}')

    def duty(self):
        '''узнаем задолжности по услугам в каждом месяце'''
        os.mkdir('не оплачены')
        for month in months:
            os.mkdir(f'не оплачены/{month}')
        for service in set_service:
            for month in months:
                duty_directory = [directory.split('_')[0].strip().replace('\ufeff', '')
                                  for directory in os.listdir(f'sorted_directory/{month}')]
                if not service in duty_directory:
                    # os.mkdir(f'не оплачены/{month}/{service}')
                    document = ap.Document()
                    page = document.pages.add()
                    text_fragment = ap.text.TextFragment(service)
                    page.paragraphs.add(text_fragment)
                    document.save(f'не оплачены/{month}/{service}.pdf')

    def delete_all_category(self):
        '''удаление всех созданных файлов и папок с компьютера'''
        directorys = ["checks", "sorted_directory", "не оплачены"]
        for directory in directorys:
            try:
                shutil.rmtree(f"{directory}")
            except:
                continue


chek = Checks()
# chek.file_simulation()
# chek.new_catalog()
# chek.scan_directory_service()
# chek.scan_directory()
# chek.duty()
chek.delete_all_category()
