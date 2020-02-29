#   CS 1XA3 Project01 - <guox54>

## Usage
    Execute this script from project root with:
        chmod +x CS1XA3/Project01/project_analyze.sh
        ./CS1XA3/Project01/project_analyze 
        and it would provide available options with number, users can enter a number, then the script would run it 



## Feature 01
Description: this feature  would find the latest commit with message cotaining "merge" and reset the reset the repo state back to the time when the commit was made
Execution: execute this feature by entering 1, followed by enter
Reference: https://stackoverflow.com/questions/19176359/how-to-get-the-last-commit-id-of-a-remote-repo-using-curl-like-command

## Feature 02
Description: this feature would list all the files in the repo with readable size and in descending order based on their size
Execution: execute this feature by entering 2
Reference: some code was taken from https://linuxize.com/post/du-command-in-linux/


## Feature 03
Description: this feature count the number of files which user can specify what kind of type they should be.
Execution: execute this feature by entering number 3


## Feature 04
Description: find all python files with the lines that contain #FIXME and put those files into fixme.log
Execution: execute this feature by entering number 4

## Feature 05
Description: find the word entered by users and loop through all python files to put thoes python files that contain the word with # in the head of the line , put the files name with those string into tag.log where tag is the world users type.
Execution: execute this feature by entering number 5

## Feature 06
Description: Users can choose to do the "Change“ action, which will add the exectuable permission to  the speicified files's class if they have the write permission; Or Users can choose to do the "Restore" action, which will restore the original permission of the files. 
Execution: execute this feature by entering number 6
Reference:https://www.linuxquestions.org/questions/linux-general-1/using-cut-on-file-full-of-ls-l-output-to-display-only-filenames-836812/
Reference : https://www.cyberciti.biz/faq/get-octal-file-permissions-from-command-line-on-linuxunix/


## Feature 07
Description: User can either choose "Backup" or "Restore". For the "Backup", it will find all the files end with .tmp and
move them into ./CS1XA3/Project01/backup/ while store the original position of those files; for the "Restore", it will re-move those files to their original position 
Execution: execute this feature by entering number 7            

## Feature 08
Description: User can either choose "Fix"(Recommend run it first time otherwise u don't know which python files contain errors) or "Restore". For "Fix", the script will collect all python  files that contain errors  under the current directory and mv them to ./CS1XA3/Project01/error_python_files and store their original position in the restore.log. Once users fix all of them , they can run the script again and choose "Restore" to put them back in their original position.
Execution: execute this feature by entering number 8

## Feature 09
Description: this feature would return the current and next two days weather of the city user want to search for.
Execution: execute this feature by entering number 9



