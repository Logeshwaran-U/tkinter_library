import os

rd = os.popen('pip list').read()
mdl1 = 'tkcalendar' in rd
mdl2 = 'mysql-connector-python' in rd
mdl3 = 'pyinstaller' in rd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'widget_images', 'books.ico')

chk = 0
if mdl1 and mdl2 and mdl3:
    try:
        print("Ensure that you changed the correct password in the source File (library.py)")
        print("The program is ready to install")
        a = input("press(y/n): ")
        if a.lower() == 'y':
            os.system(f'cmd /k "pyinstaller --noconsole --hidden-import babel.numbers --hidden-import tzdata --icon={ICON_PATH} library.py"')
        else:
            print("aborted")
    except Exception:
        print("something went wrong")
        pass
else:
    try:
        print("Packages missing\nDownload the packages via following command, using cmd:\n")
        lst = ['tkcalendar', 'mysql-connector-python', 'pyinstaller']
        if not mdl1 and not mdl2 and not mdl3:
            for pkg in lst:
                print(f"pip install {pkg}")
        else:
            if not mdl1:
                print("pip install", lst[0])
            if not mdl2:
                print("pip install", lst[1])
            if not mdl3:
                print("pip install", lst[2])
    except Exception:
        pass
