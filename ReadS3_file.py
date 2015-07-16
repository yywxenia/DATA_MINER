import csv
import os

#Parse the .csv file to get the id of projects

ID2Read=[]
with open('./proj_run_timeN.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ID2Read.append(row['ID'])
print ID2Read
print len(ID2Read)


#Parse user.txt folders in S3

userFile=[]
for i in [1,2,3,6,7,8,9,10,11,12,13,14]:
    userFile.append('user'+str(i)+'.txt')
print userFile

userDic={}
for item in userFile:
    with open (item) as f:
        content=f.readlines()
    for lines in content:
        pos1=lines.find('PRE')
        targets=lines[pos1+4:]
        IDs=targets[:4]

        if len(item)>9: ## eg. item = user12.txt (=10)
            userDic[IDs]='user-'+item[4]+item[5]+'/'+targets[:-1]
        else:
            userDic[IDs]='user-'+item[4]+'/'+targets[:-1] # eg. user-2/3117-1430173324-ATDCoffice112


#Check whiether ID is inside of the dic

for IDs in ID2Read:
    if IDs in userDic: # To check if IDs are in userDic dictionary
        pass
    else:
        print "not found ", IDs


# Generate a result folder

os.system('rm -r ./Result')
os.system('mkdir ./Result')

for IDs in ID2Read:
    print 'Processing ID: ', IDs

    DestPath =' ./Result/' + IDs +'/'  # For saving files to Result/id/
    os.system('mkdir' + DestPath) # eg. mkdir Result/id/


# Copy files into ID files under the Result folder:
### (1) for ReconstructionResult .ply
    s3path = 'pointivo-jobs/' + userDic[IDs] + 'ReconstructionResult/'

    # Generate s3 file prefix
    tmp = userDic[IDs]
    pos2 = tmp.find('/', 1)
    s3filePrefix = tmp[pos2+1: -1]

    cmd2run = 'aws s3 cp s3://' + s3path + 'Lines.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'PointsPLY.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'EdgePoints.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'Dense-Point-Cloud.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix + '-Dense-Point-Cloud-Noise-Filtered.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix + '-Dense-Point-Cloud.ply' + DestPath
    os.system(cmd2run)

### (2) for Reconstruction Result .ply
    s3path = 'pointivo-jobs/' + userDic[IDs] + '\'Reconstruction Result\'/'

    cmd2run = 'aws s3 cp s3://' + s3path + 'Lines.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'PointsPLY.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'EdgePoints.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + 'Dense-Point-Cloud.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix + '-Dense-Point-Cloud-Noise-Filtered.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix + '-Dense-Point-Cloud.ply' + DestPath
    os.system(cmd2run)

### (3) for Out .ply
    s3filePrefix2 = s3filePrefix[0:4]+'_'+s3filePrefix

    s3path = 'pointivo-jobs/' + userDic[IDs] + 'Out/'

    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix2 + '_LINE_3D.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix2 + '_POINT_DENSE.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix2 + '_POINT_DENSE__FILTERED.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix2 + '_POINT_EDGE.ply' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + s3path + s3filePrefix2 + '_POINT_DENSE__LINE_3D__FILTERED.ply' + DestPath
    os.system(cmd2run)

### (4) for logs and videos
      ##log:
    cmd2run = 'aws s3 cp s3://' + 'pointivo-jobs/' + userDic[IDs] + 'PV.CoreSFM.CoreStructureAPILog.txt' +DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + 'pointivo-jobs/' + userDic[IDs] + 'Log.txt' + DestPath
    os.system(cmd2run)
    cmd2run = 'aws s3 cp s3://' + 'pointivo-jobs/' + userDic[IDs] + 'Console\ output.txt' + DestPath
    os.system(cmd2run)

    ## videos:
    tmp2 = userDic[IDs]

    cmd2run = 'aws s3 cp s3://' + 'pointivo-jobs/' + userDic[IDs] + 'In/' + s3filePrefix2 + '_VIDEO.avi' + DestPath
    os.system(cmd2run)


print 'DONE'












