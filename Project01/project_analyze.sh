#!/bin/bash


echo -e "Option 1: find the latest merge execution and checkout.
Option 2: List all the files in repo with their size in the desceding order.
Option 3: Count the number of the file with the specific extension you want to search for .
Option 4: Find all files that contain #FIXME in their last line and put filenames into the fixme.log
Option 5: Find all python files that have lines containing the word typed by uesers and beginning with #, put those lines with the filename in to tag.log where tag is provided by users
Option 6: Either type Restore or Change with case-sensitve. Action restore will restore the file to their original permission as recored in the permissions.log; action Change will modify the files'class permission so that for each class of the file, if they have write permission, they will be added with a executable permission 
Option 7: Either type Backup or Restore, both of which will be executed on file ending with .tmp
Option 8: Fix will find all python files that have errors and move them into directory; Restore will move them back to their original position
Option 9: You can get the weather of one city  in next two days or you can just compare two cities' weather in next couple days.\n"
read -p  "Type the option number you want to execute. followed by [ENTER]:" option


#file=~/fixme.log
#> "$file"

#for f in $(find ~ -type f )
#do
#    if [[ $(tail -n 1 "$f") == *"#FIXME"* ]]; then 
#        echo "$f"
#    fi
#done

if [ $option == 1 ]; then
    cd ./CS1XA3 
    x=$(git log --oneline --graph  | grep -i "merge" | head -1)
    echo "$x"
    list=$(git log --format="%h")

    for i in $list;
    do 
    
        if [[ "$x" == *"$i"* ]]; then
            git checkout $i
        fi
    done

fi

if [ $option == 2 ]; then
    find ./CS1XA3 -type f | xargs -i du -ha '{}' | sort -h -r
fi




if [ $option == 3 ]; then
    read -p  "Type the type of file u want to count for such as py, pdf, etc [ENTER]:" x

    find  ./CS1XA3 -iname "*.$x" | wc -l
fi

if [ $option == 4 ]; then
    > ./CS1XA3/Project01/fixme.log

    for f in $(find ./CS1XA3 -type f)
    do
        if [[ $(tail -n 1 $f | grep "#FIXME") ]]; then 
            echo $f >> ./CS1XA3/Project01/fixme.log
        fi
    done

fi

if [ $option == 5 ]; then
    read -p  "Type any single word as a tag that you want to search for in python files followed by [ENTER]:" tag
    
    > ./CS1XA3/Project01/$tag.log

    for f in $(find ./CS1XA3 -name "*.py" -type f)
    do
        if [[ $(grep -E "#.*$tag.*" $f) ]]; then
            echo $f >> ./CS1XA3/Project01/$tag.log
            grep -E "#.*$tag.*" $f >> ./CS1XA3/Project01/$tag.log
            echo "" >> ./CS1XA3/Project01/$tag.log            
        fi
    done
fi

if [ $option == 6 ]; then
    read -p "Type Restore or Change followed by [ENTER]:"  execution

    if [ ! -f ./CS1XA3/Project01/permissions.log ];then
        > ./CS1XA3/Project01/permissions.log
    fi

    if [[ $execution == "Change" ]]; then
            > ./CS1XA3/Project01/permissions.log
            for f in $(find ./CS1XA3 -name "*.sh" -type f)
            do
                #echo $f
                #ls -l $f | awk '{ print $1}'

                #check user's permission
                if [[ $(ls -l $f | awk '{ print $1}') == -?w* ]]; then
                    #echo "user's worked"
                    chmod u+x $f
                    #ls -l $f
                fi
                #check group's permission
                if [[ $(ls -l $f | awk '{ print $1}') == -????w* ]]; then
                    #echo "group's worked"
                    chmod g+x $f
                    #ls -l $f
                fi
                #check other's permission
                if [[ $(ls -l $f | awk '{ print $1}') == -???????w? ]]; then
                    #echo "other's worked"
                    chmod o+x $f
                    #ls -l $f
                fi
                stat -c '%A %a %n' $f >> ./CS1XA3/Project01/permissions.log
            done
    fi

    if [[ $execution == "Restore" ]]; then
        for f in $(find ./CS1XA3 -name "*.sh" -type f)
        do
            p=$(cat ./CS1XA3/Project01/permissions.log | grep "$f" | awk '{ print $2}')
            chmod $p $f
        done
    fi
fi
if [[ $option == 7 ]]; then
    read -p "Type Restore or Backup followed by [ENTER]:"  execution
    
    if [[ $execution == "Backup" ]]; then
        if [ -d ./CS1XA3/Project01/backup ]; then
            rm -r ./CS1XA3/Project01/backup
            mkdir ./CS1XA3/Project01/backup
        else
            mkdir ./CS1XA3/Project01/backup
        fi
        
        for f in $(find ./CS1XA3 -type f -name "*.tmp" )
        do
            echo $f >> ./CS1XA3/Project01/backup/restore.log
            cp $f ./CS1XA3/Project01/backup
            rm $f

        done
    fi
    
    if [[ $execution == "Restore" ]]; then
        if [ -f ./CS1XA3/Project01/backup/restore.log ];then
            
            for f in $(ls ./CS1XA3/Project01/backup )
            do
                
                if [[ $f == *.tmp ]]; then
                    old=$(grep $f ./CS1XA3/Project01/backup/restore.log)
                    #echo $old
                    mv ./CS1XA3/Project01/backup/$f $old
                fi
            
            done
        else
            echo "./CS1XA3/Project01/backup/restore.log doesn't exist"
        fi
    fi
fi


if [ $option == 8 ]; then
    read -p  "Type  Fix or Restore followed by [ENTER]:" choice
    


    if [[ $choice == "Fix" ]]; then
        > ./CS1XA3/Project01/error.log

        if [ -d  ./CS1XA3/Project01/error_python_files ];then
            rm -r  ./CS1XA3/Project01/error_python_files
            mkdir ./CS1XA3/Project01/error_python_files        
        else
            mkdir ./CS1XA3/Project01/error_python_files
        fi
    

        for f in $(find ./CS1XA3 -name "*.py" -type f)
        do
            python $f 2>> ./CS1XA3/Project01/error.log
            echo "" >>  ./CS1XA3/Project01/error.log
        done

        > ./CS1XA3/Project01/error_python_files/backup.log



        for f in $(find ./CS1XA3 -name "*.py" -type f)
        do
            if [[ $(grep $f  ./CS1XA3/Project01/error.log) ]]; then
                echo $f > ./CS1XA3/Project01/error_python_files/backup.log
                mv $f ./CS1XA3/Project01/error_python_files
            fi
        done
    fi

    if [[ $choice == "Restore" ]]; then

        if [ -f ./CS1XA3/Project01/error.log ]; then 
            
            for f in $(ls ./CS1XA3/Project01/error_python_files )
            do
                if [[ $f = *.py ]]; then
                    old=$(grep $f ./CS1XA3/Project01/error_python_files/backup.log)
                    mv ./CS1XA3/Project01/error_python_files/$f $old

                fi
            done
            
        else
            echo "There doesn't exist ./CS1XA3/Project01/error.log "
        fi
    fi

fi  


if [ $option == 9 ]; then
    read -p  "If u just want to see the wearther of a city just type 1 or u want to compare two cities weather type 2 followed by [ENTER]:" choice
    if [[ $choice == 1 ]];then
        read -p  "Type  the name of city followed by [ENTER]:" city
        curl -s http://wttr.in/$city
        
    fi
    if [[ $choice == 2 ]];then
        read -p  "Type  the name of first city followed by [ENTER]:" city1
        read -p  "Type  the name of second city followed by [ENTER]:" city2
        diff -Naur <(curl -s http://wttr.in/$city1 ) <(curl -s http://wttr.in/$city2 )        
    fi
fi