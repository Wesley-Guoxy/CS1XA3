#!/bin/bash


echo -e "Option 2: find the latest merge execution and checkout.
Option 3: List all the files in repo with their size in the desceding order.
Option 4: Count the number of the file with the specific extension you want to search for .\n"
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
    x=$(git log --oneline --graph | grep -i "merge" | head -1)
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
