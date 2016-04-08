##—————————————阈值判决模块—————————————
##用于在接收一帧数据之前，判断这帧数据是否是有效动作，若有则接收13帧（待定）
##否则继续判决下一帧

def isReceive(testFrameData):
    Flag=False
    Gates=None#阈值门限
    #用一个或几个加速度大小来判断，kkkk为指代
    if testFrameData[kkkk]>Gates[kkkk]:
        Flag=True

    return Flag
