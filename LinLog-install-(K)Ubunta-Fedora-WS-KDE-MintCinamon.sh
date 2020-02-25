#!/bin/bash
name_app='linlog'
git_path='https://github.com/bastonc/linlog_v1.1.git'
de=$XDG_CURRENT_DESKTOP
#echo $de
dist=`cat /etc/*release | grep -w NAME`
dist_name_dirty=${dist:5}
dist_name=${dist_name_dirty//\"/}
clear
if [[ "$de" == 'KDE' && "$dist_name" == 'Fedora' ]]
then
  echo -en "\n\nSorry, system using $de into $dist_name. \n\nCan't continue, because - package python3-qt5 destroed $de into Fedora.\n\nToday (24 feb 2020) Fedora have this bug. If you installing LinLog much later, meybe it fixed.\nIf you understand effects - you can enter string \"Understand\", else press any key\n\n\n"
  echo -en "LinLog installation: ->>"
  read flag
    if [[ "$flag" == "Understand" ]]
    then
      echo -en "\n\nOK!\n\n\n Download python3-qt5-5.13.2-3.fc31.i686.rpm"
      cd ~
      wget http://rpmfind.net/linux/fedora/linux/updates/31/Everything/x86_64/Packages/p/python3-qt5-5.13.2-3.fc31.i686.rpm && sudo dnf install python3-qt5-5.13.2-3.fc31.i686.rpm
    else
      echo "===============-- Cancel installation. --================="
      exit 0
    fi
else
  echo -en "\nGood! Continue\n\n"
  fi
    echo $dist_name

  # check git
  if [[ `git --version` -eq 0 ]]
  then
    if [[ "$dist_name" == "LinuxMint" || "$dist_name" == "Ubuntu" || "$dist_name" == "\"Ubuntu\"" || "$dist_name" == "Xubuntu" || "$dist_name" == "Lubuntu" || "$dist_name" == "Lubuntu" || "$dist_name" == "Debian" ]]
    then
        sudo apt install git # if git not installed - install it
    fi
    if [[ "$dist_name" == "Fedora" || "$dist_name" == "Rad-hat" || "$dist_name" == "CentOS" ]]
    then
        sudo dnf install git # if git not installed - install it
    fi
  else
      echo -en '\n\ngit installed to you system\n'
      echo -en `git --version`'\n\n'
  fi

#download repository and enter in dir
cd $HOME
if git clone $git_path $name_app
then
#echo "Download source code from git repository"
cd ./$name_app
else
echo -en "\n\nDir $name_app not empty or git not install.\n\n\n"
exit 1  
fi

#setup all depensies 

if [[ "$dist_name" == "LinuxMint" || "$dist_name" == "Ubuntu" || "$dist_name" == "\"Ubuntu\"" || "$dist_name" == "Xubuntu" || "$dist_name" == "Lubuntu" || "$dist_name" == "Lubuntu" || "$dist_name" == "Debian" ]]
then
echo -en '\n\n=======- Install all dependisesn -===========\n\n'
sudo apt install python3-pip && sudo apt install python3-pyqt5 && sudo pip3 install datetime && sudo pip3 install urllib3 && sudo pip3 install websocket-client2 && sudo pip3 install bs4 && sudo pip3 install telnetlib3
echo -en "\n\n=====- Dependenses insatalled -=======\n\n"
fi
if [[ "$dist_name" == "Fedora" || "$dist_name" == "Rad-hat" || "$dist_name" == "CentOS" ]]
then
# && sudo dnf install python3-qt5
#http://rpmfind.net/linux/fedora/linux/updates/31/Everything/x86_64/Packages/p/python3-#qt5-5.13.2-3.fc31.i686.rpm
if [[ "$dist_name" == 'Fedora' ]]
then
  if [[ "$de" != 'KDE' && "$dist_name" == 'Fedora' ]]
    then
      sudo dnf install python3-qt5
    fi
else
    sudo dnf install python3-qt5
fi

echo -en '\n\n=======- Install all dependisesn -===========\n\n'
#sudo pip3 uninstall websocket-client && sudo pip3 install websocket-client2 &&
sudo dnf install python3-pip && sudo pip3 install datetime && sudo pip3 install urllib3 && sudo pip3 install websocket && sudo pip3 install websocket-client2 && sudo pip3 install bs4 && sudo pip3 install telnetlib3
echo -en "\n\n=====- Dependenses insatalled -=======\n\n"
fi
echo -en "\n\nCreating run file\n\n"
# Create run file
cat > $HOME/$name_app/linlog << EOF
#!/bin/bash
cd $HOME/$name_app/
python3 main.py
EOF
if [[ `chmod +x $HOME/$name_app/linlog` -ne 0 ]]
then
echo -en "\nERROR: Can't setup executable bit\n\n"
exit 1
fi
echo -en "Creating desktop file\n\n"
# Create desktop.file
cat > $HOME/$name_app/linlog.desktop << EOF
[Desktop Entry]
Name=LinLog
Comment=Do it
Exec= $HOME/$name_app/linlog
Icon=$HOME/$name_app/icon.svg
Terminal=false
Type=Application
Categories=AmateurRadio;
EOF

destination='/usr/share/applications'
echo "copying linlog.desktop file to $destination "
sudo cp $HOME/$name_app'/linlog.desktop' $destination
#fi

echo -en "\n\n ======- Install complited -=======\n\n"

exit 0



