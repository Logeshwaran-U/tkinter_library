import os
rd=os.popen('pip list').read()
mdl1='tkcalendar' in rd
mdl2='mysql-connector-python' in rd
mdl3='pyinstaller' in rd
chk=0
if mdl1 and mdl2 and mdl3:
    try:
        print("Ensure that you  changed the correct password in the source File(library)")
        print("The  program is ready to install")
        a=input("press(y/n):")
        if a.lower()=='y':
            os.system('cmd /k "pyinstaller --noconsole --hidden-import "babel.numbers" --hidden-import "tzdata"  --icon=books.ico library.py " ')
        else:
            print("aborted")
    except Exception:
        print("something went wrong")
        pass
else:
    try:
        print("packages missing\nDownload the packages via following command,using cmd:\n")
        lst=['tkcalendar','mysql-connector-python','pyinstaller']
        if mdl1==False and mdl2==False and mdl3==False:
            for pkg in lst:
                print("pip install {}".format(pkg))
        else:
            if mdl1==False:
                print("pip install",lst[0])
            if mdl2==False:
                print("pip install",lst[1])
            if mdl3==False:
                print("pip install",lst[2])
    except Exception:
        pass        
