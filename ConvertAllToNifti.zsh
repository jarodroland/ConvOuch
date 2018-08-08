#! /bin/zsh

IFS=$'\n'

for studyFolder in $(cat GoodDicomFolderList.txt); do
    subject=$studyFolder:h:h:t:t:t
    outDir="/Volumes/My4TB/CQ500/NiftiFiles/"
    
    if [ ! -d ${(q)outDir}${(q)subject} ] 
    then
        mkdir ${(q)outDir}${(q)subject}
    fi
    
    #temp=$(printf %q "$studyFolder")   # bash way of escaping
    #temp=${(q)studyFolder}/*.dcm       # zsh way of escaping
    #echo "ls $temp"

    echo "dcm2niix -z y -m y -o ${(q)outDir}${(q)subject}/ ${(q)studyFolder}/*.dcm"
done
